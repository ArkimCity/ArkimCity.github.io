# tested with python 3.11
# torch==2.6.0
# numpy==2.2.3
# pygad==3.4.0

import os
from typing import List
from enum import Enum, auto

import torch
import numpy as np
import pygad

import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class OptimizerMode(Enum):
    GA = auto()
    SIMPLE_GRADIENT_DESCENT = auto()
    ADAMW = auto()


class EnvironmentMode(Enum):
    NO_GRADIENT_CUTOFF = auto()
    DEFINITE_GRADIENT_CUTOFF = auto()


def get_intersection_area(rect1: torch.Tensor, rect2: torch.Tensor, buffer: float = 0.1) -> torch.Tensor:
    buffered_rect_1 = (rect1[0] - buffer, rect1[1] - buffer, rect1[2] + buffer, rect1[3] + buffer)
    buffered_rect_2 = (rect2[0] - buffer, rect2[1] - buffer, rect2[2] + buffer, rect2[3] + buffer)

    # 두 사각형의 교차 영역 계산
    x1 = torch.maximum(buffered_rect_1[0], buffered_rect_2[0])
    y1 = torch.maximum(buffered_rect_1[1], buffered_rect_2[1])

    x2 = torch.minimum(buffered_rect_1[2], buffered_rect_2[2])
    y2 = torch.minimum(buffered_rect_1[3], buffered_rect_2[3])

    w = torch.relu(x2 - x1)
    h = torch.relu(y2 - y1)

    return w * h


def get_loss(
    boundary_bounds: torch.Tensor,
    rectangles_bounds: torch.Tensor,
    target_aspect_ratio: float,
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:

    assert boundary_bounds.shape == (4,)
    assert (rectangles_bounds >= 0).all(), f"rectangles_bounds: {rectangles_bounds}"

    # 각 사각형의 넓이를 계산
    rectangles_areas = (
        rectangles_bounds[:, 2] - rectangles_bounds[:, 0]
    ) * (
        rectangles_bounds[:, 3] - rectangles_bounds[:, 1]
    )

    # loss 1 - 각 사각형의 넓이의 분산을 계산
    loss_1 = torch.mean((rectangles_areas - rectangles_areas.mean()) ** 2)

    # loss 2 - 각 사각형의 서로 겹치는 넓이의 합을 계산
    n = len(rectangles_bounds)
    idx1, idx2 = torch.triu_indices(n, n, offset=1)
    intersection_area_sum = torch.tensor(0.0)
    for i, j in zip(idx1, idx2):
        intersection_area_sum += get_intersection_area(
            rectangles_bounds[i],  # (n*(n-1)/2, 4)
            rectangles_bounds[j]   # (n*(n-1)/2, 4)
        )
    loss_2 = intersection_area_sum

    # loss 3 - 각 사각형의 aspect_ratio 가 target_aspect_ratio 에 가까워야 한다.
    loss_3 = (
        (
            (rectangles_bounds[:, 2] - rectangles_bounds[:, 0])
            / (rectangles_bounds[:, 3] - rectangles_bounds[:, 1])
        ) - target_aspect_ratio
    ).abs().sum()

    # loss 5 - 전체 사각형 면적은 커져야 한다.
    loss_4 = -rectangles_areas.sum() / 2

    return loss_1 + loss_2 + loss_3 + loss_4, {
        "loss_1": loss_1,
        "loss_2": loss_2,
        "loss_3": loss_3,
        "loss_4": loss_4,
    }


def get_coords_from_bounds(bounds: torch.Tensor) -> torch.Tensor:
    return torch.stack(
        [
            torch.stack([bounds[0], bounds[1]]),
            torch.stack([bounds[2], bounds[1]]),
            torch.stack([bounds[2], bounds[3]]),
            torch.stack([bounds[0], bounds[3]]),
            torch.stack([bounds[0], bounds[1]]),
        ]
    )


def plot_loss_graph(optimizer_mode: OptimizerMode, loss_history: list[float], file_path: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    line, = ax.plot([], [], 'b-')

    # 그래프 설정
    ax.set_xlim(0, len(loss_history))
    ax.set_ylim(min(loss_history), max(loss_history))
    if optimizer_mode == OptimizerMode.GA:
        ax.set_xlabel('Generation')
    elif optimizer_mode in [OptimizerMode.SIMPLE_GRADIENT_DESCENT, OptimizerMode.ADAMW]:
        ax.set_xlabel('Epoch')
    else:
        raise ValueError(f"Invalid optimizer mode: {optimizer_mode.value}")

    ax.set_ylabel('Loss')
    ax.set_title('Training Loss')

    def init():
        line.set_data([], [])
        return line,

    def animate(frame):
        line.set_data(range(frame + 1), loss_history[:frame + 1])
        return line,

    # 애니메이션 생성
    anim = animation.FuncAnimation(
        fig, animate, init_func=init, frames=len(loss_history), interval=50, blit=True
    )

    # GIF로 저장
    anim.save(file_path, writer='pillow')
    plt.close()


def plot_animation(
    file_path: str,
    boundary_coords: np.ndarray,
    rectangles_coords_history: List[np.ndarray],
):
    # create gif of core_center_history
    frames = []
    fig, ax = plt.subplots(figsize=(4, 4))

    for each_rectangle_coords_history in rectangles_coords_history:
        ax.clear()

        # boundary 표시 및 영역 설정
        boundary_x_length = boundary_coords[:, 0].max() - boundary_coords[:, 0].min()
        boundary_y_length = boundary_coords[:, 1].max() - boundary_coords[:, 1].min()
        boundary_x_buffer = boundary_x_length * 0.1
        boundary_y_buffer = boundary_y_length * 0.1
        ax.set_xlim(boundary_coords[:, 0].min() - boundary_x_buffer, boundary_coords[:, 0].max() + boundary_x_buffer)
        ax.set_ylim(boundary_coords[:, 1].min() - boundary_y_buffer, boundary_coords[:, 1].max() + boundary_y_buffer)
        ax.plot(boundary_coords[:, 0], boundary_coords[:, 1], "k-", label="Boundary")

        # grid box 표시
        for each_rectangle_coords in each_rectangle_coords_history:
            rectangle = plt.Polygon(each_rectangle_coords, fill=False, color="red", label="Rectangle")
            ax.add_patch(rectangle)

        # 프레임 저장
        plt.axis("off")
        fig.canvas.draw()
        image = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(image)

    # GIF 저장
    imageio.mimsave(file_path, frames, duration=0.02)


def get_rectangles_bounds_with_x_y_ratio(
    parameters: torch.Tensor,
    boundary_bounds: torch.Tensor,
    num_rectangles: int,
) -> torch.Tensor:
    """파라미터를 x,y 위치 좌표 ratio로 변환하여 사각형의 좌표를 계산한다."""
    rectangles_infos: torch.Tensor = parameters.reshape(num_rectangles, 2, 2)  # (4개 사각형, [position, size], [x, y])

    # 각 사각형의 좌표를 계산 (x1,y1,x2,y2)
    positions = rectangles_infos[:, 0, :] * boundary_bounds[2:]
    sizes = rectangles_infos[:, 1, :].abs() * (boundary_bounds[2:] - positions)
    return torch.cat([positions, positions + sizes], dim=1)  # shape: (num_rectangles, 4)


def get_position(p: torch.Tensor, boundary_bounds: torch.Tensor) -> torch.Tensor:
    assert p.shape == (2,)

    position_parameter = p[0]
    offset_parameter = p[1]

    x_min, y_min, x_max, y_max = boundary_bounds
    width = x_max - x_min
    height = y_max - y_min

    total_length = (width + height)

    p_length = position_parameter * total_length

    if p_length < width / 2:
        offset_vector = torch.stack([torch.tensor(0.0), offset_parameter * height * 0.5])
        base_position = torch.stack([x_min + p_length, y_min])
    elif p_length < (width + height) / 2:
        offset_vector = torch.stack([-offset_parameter * width * 0.5, torch.tensor(0.0)])
        base_position = torch.stack([x_max, y_min + (p_length - width / 2)])
    elif p_length < (width + height + width) / 2:
        offset_vector = torch.stack([torch.tensor(0.0), -offset_parameter * height * 0.5])
        base_position = torch.stack([x_max - (p_length - (width + height) / 2), y_max])
    else:
        offset_vector = torch.stack([offset_parameter * width * 0.5, torch.tensor(0.0)])
        base_position = torch.stack([x_min, y_max - (p_length - (width + height + width) / 2)])

    return base_position + offset_vector


def get_rectangle_bounds_with_interpolation_offset(
    parameters: torch.Tensor,
    boundary_bounds: torch.Tensor,
    num_rectangles: int,
) -> torch.Tensor:
    """파라미터를 interpolation offset 으로 변환하여 사각형의 좌표를 계산한다."""
    rectangles_infos: torch.Tensor = parameters.reshape(num_rectangles, 2, 2)  # (4개 사각형, [position, size], [x, y])

    positions = torch.stack([get_position(p, boundary_bounds) for p in rectangles_infos[:, 0, :]])
    sizes = rectangles_infos[:, 1, :].abs() * (boundary_bounds[2:] - positions)

    return torch.cat([positions, positions + sizes], dim=1)


def run_single(
    environment_mode: EnvironmentMode,
    using_parameters: torch.Tensor,
    boundary_bounds: torch.Tensor,
    num_rectangles: int,
    target_aspect_ratio: float,
    loss_history: list[float],
    loss_details_history: list[dict[str, float]],
    rectangles_coords_history: list[np.ndarray],
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """parameter 를 이용해 4각형 4개 좌표를 도출하고, loss를 계산한다."""

    if environment_mode == EnvironmentMode.NO_GRADIENT_CUTOFF:
        # 파라미터를 x,y 위치 좌표 ratio로 변환하여 사각형의 좌표를 계산한다.
        rectangles_bounds = get_rectangles_bounds_with_x_y_ratio(using_parameters, boundary_bounds, num_rectangles)
    else:
        # 파라미터를 interpolation offset 으로 변환하여 사각형의 좌표를 계산한다.
        rectangles_bounds = get_rectangle_bounds_with_interpolation_offset(
            using_parameters, boundary_bounds, num_rectangles
        )

    rectangles_coords = torch.stack(  # shape: (num_rectangles, 5, 2)
        [
            get_coords_from_bounds(rectangles_bounds[i]) for i in range(num_rectangles)
        ]
    )

    # loss - make sure tensor connection is valid from core_coords to loss
    loss, loss_details = get_loss(boundary_bounds, rectangles_bounds, target_aspect_ratio)

    loss_history.append(loss.item())
    loss_details_history.append({key: each_loss.item() for key, each_loss in loss_details.items()})
    rectangles_coords_history.append(rectangles_coords.detach().numpy())

    return loss


def ga_fitness_func(ga_instance: pygad.GA, solution: torch.Tensor, _: int) -> float:

    current_generation = ga_instance.generations_completed

    boundary_bounds = ga_instance.boundary_bounds
    num_rectangles = ga_instance.num_rectangles
    target_aspect_ratio = ga_instance.target_aspect_ratio
    environment_mode = ga_instance.environment_mode
    loss_history = ga_instance.loss_history_list[current_generation]
    loss_details_history = ga_instance.loss_details_history_list[current_generation]
    rectangles_coords_history = ga_instance.rectangles_coords_history_list[current_generation]

    using_parameters = torch.tensor(solution)

    loss = run_single(
        environment_mode,
        using_parameters,
        boundary_bounds,
        num_rectangles,
        target_aspect_ratio,
        loss_history,
        loss_details_history,
        rectangles_coords_history,
    )

    # ga 는 Loss 가 아닌 score 방식으로, 음수를 곱해줍니다
    return -loss.item()


def main():
    # mode settings
    optimizer_mode = OptimizerMode.SIMPLE_GRADIENT_DESCENT
    environment_mode = EnvironmentMode.NO_GRADIENT_CUTOFF

    # environment settings
    boundary_size_x = 5
    boundary_size_y = 5
    num_rectangles = 4
    target_aspect_ratio = 1.5

    # optimizer settings
    learning_rate = 0.05
    epoch = 200

    # boundary 정의
    boundary_bounds: torch.Tensor = torch.tensor([0, 0, boundary_size_x, boundary_size_y])
    boundary_coords = get_coords_from_bounds(boundary_bounds)

    # 사각형 4개에 해당하는 x,y position size ratio parameter 를 정의한다. - 총 16개의 parameter 를 정의한다.
    torch.manual_seed(123)
    parameters: torch.Tensor = torch.randn(num_rectangles * 2 * 2, requires_grad=True)

    if optimizer_mode == OptimizerMode.GA:
        num_generations = 200
        loss_history_list: List[List[float]] = [[] for _ in range(num_generations + 1)]
        loss_details_history_list: List[List[dict[str, float]]] = [[] for _ in range(num_generations + 1)]
        rectangles_coords_history_list: List[List[np.ndarray]] = [[] for _ in range(num_generations + 1)]

        ga_optimizer = pygad.GA(
            num_generations=num_generations,
            sol_per_pop=100,
            num_parents_mating=10,
            fitness_func=ga_fitness_func,
            num_genes=num_rectangles * 2 * 2,
            gene_space=[{"low": 0, "high": 1} for _ in range(num_rectangles * 2 * 2)],  # 각 유전자가 0~1 범위
        )
        ga_optimizer.boundary_bounds = boundary_bounds
        ga_optimizer.num_rectangles = num_rectangles
        ga_optimizer.target_aspect_ratio = target_aspect_ratio
        ga_optimizer.environment_mode = environment_mode
        ga_optimizer.loss_history_list = loss_history_list
        ga_optimizer.loss_details_history_list = loss_details_history_list
        ga_optimizer.rectangles_coords_history_list = rectangles_coords_history_list

        ga_optimizer.run()

        min_args = [np.argmin(x) for x in loss_history_list]

        loss_history = [loss_history_list[x][min_args[x]] for x in range(len(min_args))]
        loss_details_history = [loss_details_history_list[x][min_args[x]] for x in range(len(min_args))]
        rectangles_coords_history = [rectangles_coords_history_list[x][min_args[x]] for x in range(len(min_args))]
    elif optimizer_mode in [OptimizerMode.SIMPLE_GRADIENT_DESCENT, OptimizerMode.ADAMW]:
        loss_history: list[float] = []
        loss_details_history: list[dict[str, float]] = []
        rectangles_coords_history: list[np.ndarray] = []  # (epoch, num_rectangles, 5, 2)

        if optimizer_mode == OptimizerMode.ADAMW:
            optimizer = torch.optim.AdamW([parameters], lr=learning_rate)
        elif optimizer_mode == OptimizerMode.SIMPLE_GRADIENT_DESCENT:
            optimizer = torch.optim.SGD([parameters], lr=learning_rate)
        else:
            raise ValueError(f"Invalid optimizer mode: {optimizer_mode.value}")

        for _ in range(epoch):
            # 직접 gradent 계산하는 경우, 혹은 AdamW optimizer 를 사용하는 경우에 파라미터를 0~1 사이로 제한하기 위해 sigmoid 함수를 사용한다.
            using_parameters = torch.sigmoid(parameters)

            loss = run_single(
                environment_mode,
                using_parameters,
                boundary_bounds,
                num_rectangles,
                target_aspect_ratio,
                loss_history,
                loss_details_history,
                rectangles_coords_history,
            )

            loss.backward()  # loss backprop

            optimizer.step()
            optimizer.zero_grad()
    else:
        raise ValueError(f"Invalid optimizer mode: {optimizer_mode.value}")

    # 최종 loss 그래프 저장
    plot_loss_graph(optimizer_mode, loss_history, os.path.join(os.path.dirname(__file__), "loss_graph.gif"))

    # 최종 loss 상세 그래프 저장
    for key in loss_details_history[-1].keys():
        loss_values_for_key = [each_loss_details[key] for each_loss_details in loss_details_history]
        plot_loss_graph(optimizer_mode, loss_values_for_key, os.path.join(os.path.dirname(__file__), f"{key}_loss_graph.gif"))

    plot_animation(
        os.path.join(os.path.dirname(__file__), "animation.gif"),
        boundary_coords.detach().numpy(),
        rectangles_coords_history
    )


if __name__ == "__main__":
    main()
