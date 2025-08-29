---
layout: post
title: "가구를 배달해보자"
thumbnail: /assets/images/delivering-furniture/thumbnail.png
categories: [three.js]
tags: [kubernetes, three.js, 3d-rendering, vector, matrix, affine-transformation]  # red, yellow
featured: false
hidden: false
# beforetoc: "쿠버네티스 포드 엔진에서 도형 연산을 통한 가구 배치 계산부터 Three.js 프론트엔드 렌더링까지"
# toc: true
---


<img src="/assets/images/delivering-furniture/thumbnail.png" style="width: 800px; max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
## 개요
- 쿠버네티스 포드 엔진에서 도형 연산을 통해 가구의 최적 위치를 계산하고, 백엔드에서 이 정보를 받아 프론트엔드에서 Three.js를 사용하여 3D 모델을 배치하는 작업이 필요했습니다. 3D 모델을 직접 스트리밍하지 않고 메타데이터만 전송하여 효율성을 개선했습니다.
- cpu 사용률이 매우 높고 10초 이상 걸리는 길고 무거운 작업은 연산용 pod를 트리거합니다.
- 엔진과 백엔드 서버는 10메가바이트씩 하는 obj 파일을 수정해서 저장한 뒤 직접 보내줄 필요는 없습니다. 백엔드 서버는 수정에 필요한 벡터 및 행렬 정보만 프론트에 주면 됩니다.

## 구조

<div style="width: 800px; max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
    <img src="/assets/images/delivering-furniture/structure.png" style="max-width: 100%;">
    <div style="font-size: 10px; color: #808080; margin-top: 5px;">구조 다이어그램</div>
</div>

시스템은 다음과 같은 계층 구조로 구성됩니다:

1. **사용자 계층**: React 프론트엔드를 통해 시스템과 상호작용
2. **프론트엔드 계층**: React Three Fiber를 사용한 3D 렌더링
3. **백엔드 API 계층**: FastAPI를 통한 비동기 작업 관리
4. **하위 서비스 계층**: 쿠버네티스 포드 엔진과 S3(CloudFront CDN)

### 1. 쿠버네티스 포드 엔진 (도형 연산)

벡터와 행렬 연산을 통한 가구 배치 최적화: 가구 배치 결과와 plane 결과를 저장하는 것을 목적으로 합니다.

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Plane:
    origin: Tuple[float, float, float]
    x_axis: Tuple[float, float, float]
    y_axis: Tuple[float, float, float]

@dataclass
class FurniturePlacement:
    furniture_type: str
    name: str
    original_plane: Plane
    plane: Plane

class FurniturePlacementEngine:

    ...

    def calculate_optimal_placement(...) -> List[FurniturePlacement]:
        """
        방 크기와 가구 타입을 기반으로 최적의 배치 위치를 계산
        """
        all_placements: List[FurniturePlacement] = []
        
        ...

            all_placements.append(placement)
        
        ...

        return all_placements
    
    ...
```

### 2. 백엔드 API

쿠버네티스 엔진과의 비동기 통신을 위한 두 단계 API 구조:

**1단계: 작업 트리거 (Trigger)**
- 사용자의 가구 배치 요청을 받아 쿠버네티스 엔진에 작업을 등록
- 즉시 `jobId`와 `processing` 상태를 반환하여 응답성 확보
- CPU 집약적 연산을 백그라운드에서 처리

**2단계: 결과 확인 (Result)**
- `jobId`를 통해 작업 완료 여부를 확인
- 완료된 경우: CloudFront CDN에서 3D 모델 URL을 생성하여 배치 결과와 함께 반환
- 진행 중인 경우: `finished: false` 상태 반환
- 오류 발생 시: 에러 정보와 함께 반환

이러한 분리된 구조를 통해 사용자는 즉시 응답을 받고, 프론트엔드에서는 주기적으로 결과를 확인하여 완료 시 3D 렌더링을 수행합니다.

### 3. 프론트엔드 (Transformation Matrix 데이터를 받아 InstancedMesh로 적용)

**InstancedMesh와 Transformation Matrix를 활용한 최적화된 3D 렌더링:**

```typescript

...

interface Plane {
    origin: [number, number, number];
    x_axis: [number, number, number];
    y_axis: [number, number, number];
}

...

    // Create transformation matrices
    const originalMatrix = new THREE.Matrix4();
    const targetMatrix = new THREE.Matrix4();

    // Set up the original plane matrix
    originalMatrix.set(
      original_plane.x_axis[0], original_plane.y_axis[0], 0, original_plane.origin[0],
      original_plane.x_axis[1], original_plane.y_axis[1], 0, original_plane.origin[1],
      0, 0, 1, 0,
      0, 0, 0, 1
    );

    // Set up the target plane matrix
    targetMatrix.set(
      plane.x_axis[0], plane.y_axis[0], 0, plane.origin[0],
      plane.x_axis[1], plane.y_axis[1], 0, plane.origin[1],
      0, 0, 1, 0,
      0, 0, 0, 1
    );

    // Calculate the transformation from original to target
    const originalInverse = originalMatrix.clone().invert();
    const transformationMatrix = targetMatrix.clone().multiply(originalInverse);

    // Initialize arrays if they don't exist
    if (!this.instanceMatrices[name]) {
      this.instanceMatrices[name] = [];
    }

    // Add the transformation matrix to our array
    this.instanceMatrices[name].push(transformationMatrix);

...


```

## 성능 최적화

1. **분산 처리**: 쿠버네티스 포드 엔진에서 도형 연산을 독립적으로 처리
2. **가벼운 백엔드 통신**: 변화된 가구의 결과를 직접 파일로 전달하지 않고 Transformation Matrix 데이터를 구분해 상호작용 
3. **3D 파일 간접 전달**: 프론트엔드가 S3(CloudFront CDN)에서 3D 모델 로딩
4. **InstancedMesh 렌더링**: 동일한 가구 모델의 다중 인스턴스를 단일 드로우 콜로 처리


## 결론

이 시스템을 통해 다음과 같은 이점을 얻을 수 있습니다:

1. **효율적인 리소스 사용**: 3D 모델을 직접 스트리밍하지 않아 메인 서버의 네트워크 부하 감소
2. **확장 가능한 아키텍처**: 쿠버네티스를 통한 엔진 스케일링
3. **정확한 도형 연산**: 벡터와 행렬 연산을 통한 정밀한 위치 계산
4. **고성능 렌더링**: InstancedMesh와 Transformation Matrix를 통한 최적화된 3D 렌더링

이러한 접근 방식을 통해 대용량 3D 데이터를 효율적으로 처리하면서도 사용자에게 풍부한 3D 경험을 제공할 수 있습니다.
