---
layout: post
title:  "Observer for Architectural Element"
# author: john
categories: [ Automation ]
tags: []  # red, yellow
# image: assets/images/11.jpg
description: "설계 자동화에 필요한 코드 전략 - 옵저버 패턴"
featured: false
hidden: false
# rating: 4.5
beforetoc: "test"
toc: false
---

건축 설계 자동화 작업을 위해서는 도형 작업이 필수적입니다.
도형을 다루다 보면 어떤 도형이 변하면 그에 따른 변화를 다른 건축 요소에 적용해야 하는 경우가 수도 없이 많습니다.

이 때 각 도형을 일일히 수동으로 업데이트 하는 것은 오류를 발생시킬 여지도 많을 뿐더러 코드를 길게 만드는 요소입니다.

따라서, 어떤 건축 요소의 도형이 변화하는 것을 인지해 이에 따른 이동이 필요한 경우에 대해 자동으로 반응하도록 하는 것이 좋은데,
이 때 사용하기 적절한 컨벤션이 바로 옵저버 패턴입니다.

코어 및 코어 내부의 계단, 엘레베이터 클래스를 예시로 들어보겠습니다.
(계단과 엘레베이터는 코어 내부에 종속적인 요소임으로 코어의 기준점의 상대좌표로 사용하는 방법도 있겠습니다만, 옵저버 패턴 방식으로 이 포스트에서는 작성해 보겠습니다. 상대좌표는 추후 별도 포스트를 작성하겠습니다.)

<hr>

아래는 위 내용을 반영한 간단한 예시입니다.
- 엘레베이터와 계단의 위치는 직접 translate 하지 않습니다
- 코어의 위치가 변경 될 때 계단과 엘레베이터에 위치 변경이 전파됩니다.

```python
from abc import ABC, abstractmethod
from shapely.geometry import Polygon
from shapely.affinity import translate


class ArchitecturalElement(ABC):
    def __init__(self, polygon) -> None:
        self.__polygon = polygon

    @property
    def polygon(self) -> Polygon:
        """The 'polygon' property getter method."""
        return self.__polygon

    @polygon.setter
    def polygon(self, value) -> None:
        """The 'polygon' property setter method with validation."""
        if not isinstance(value, Polygon):
            raise ValueError("Value must be a Polygon instance.")
        self.__polygon = value

    @abstractmethod
    def translate(self, xoff, yoff):
        """shapely translation 을 수행합니다."""
        pass


class Core(ArchitecturalElement):
    def __init__(self, polygon) -> None:
        super().__init__(polygon)
        self.__observers = []

    def __repr__(self) -> str:
        return f"Core: {self.polygon.wkt}"

    def add_observer(self, observer) -> None:
        self.__observers.append(observer)

    def notify_translate(self, xoff, yoff) -> None:
        for observer in self.__observers:
            observer.translate(xoff, yoff)

    def translate(self, xoff, yoff) -> None:
        print(f"Moving polygon by x offset: {xoff}, y offset: {yoff}")
        self.polygon = translate(self.polygon, xoff=xoff, yoff=yoff)
        self.notify_translate(xoff, yoff)


class Stair(ArchitecturalElement):
    def __init__(self, polygon) -> None:
        super().__init__(polygon)

    def __repr__(self) -> str:
        return f"Stair: {self.polygon.wkt}"

    def translate(self, xoff, yoff) -> None:
        self.polygon = translate(self.polygon, xoff, yoff)


class Elev(ArchitecturalElement):
    def __init__(self, polygon) -> None:
        super().__init__(polygon)

    def __repr__(self) -> str:
        return f"Elev: {self.polygon.wkt}"

    def translate(self, xoff, yoff) -> None:
        self.polygon = translate(self.polygon, xoff, yoff)


if __name__ == "__main__":
    # 사용 예
    core_polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    stair_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    elev_polygon = Polygon([(1, 0), (2, 0), (2, 1), (1, 1), (1, 0)])

    core = Core(core_polygon)
    stair = Stair(stair_polygon)
    elev = Elev(elev_polygon)

    core.add_observer(stair)
    core.add_observer(elev)

    print(core)  # Expected: Core: POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))
    print(stair) # Expected: Stair: POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))
    print(elev)  # Expected: Elev: POLYGON ((1 0, 2 0, 2 1, 1 1, 1 0))

    core.translate(10, 20)
    print(core)  # Expected: Core: POLYGON ((10 20, 12 20, 12 22, 10 22, 10 20))
    print(stair) # Expected: Stair: POLYGON ((10 20, 11 20, 11 21, 10 21, 10 20))
    print(elev)  # Expected: Elev: POLYGON ((11 20, 12 20, 12 21, 11 21, 11 20))

    core.translate(-5, -5)
    print(core)  # Expected: Core: POLYGON ((5 15, 7 15, 7 17, 5 17, 5 15))
    print(stair) # Expected: Stair: POLYGON ((5 15, 6 15, 6 16, 5 16, 5 15))
    print(elev)  # Expected: Elev: POLYGON ((6 15, 7 15, 7 16, 6 16, 6 15))


```
