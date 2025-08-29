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

벡터와 행렬 연산을 통한 가구 배치 최적화:

```python
@dataclass
class Position3D:
    x: float; y: float; z: float

@dataclass
class FurniturePlacement:
    furniture_type: str
    position: Position3D
    rotation: Position3D  # degrees
    scale: Position3D
    confidence_score: float

class FurniturePlacementEngine:

    ...
                
                placement = FurniturePlacement(
                    furniture_type=furniture_type,
                    position=final_transform['position'],
                    rotation=final_transform['rotation'],
                    scale=final_transform['scale'],
                    confidence_score=confidence_score
                )
                all_placements.append(placement)
        
        return sorted(all_placements, key=lambda p: p.confidence_score, reverse=True)
```

### 2. 백엔드 API (비동기 처리)

쿠버네티스 엔진과의 비동기 통신:

```typescript
// 배치 요청 트리거
app.post('/api/furniture/placement', async (req, res) => {
    const jobId = await kubernetesEngine.triggerPlacementJob(req.body);
    res.json({ jobId, status: 'processing' });
});

// 결과 확인 API
app.get('/api/furniture/result/:jobId', async (req, res) => {
    const result = await kubernetesEngine.getJobResult(req.params.jobId);
    
    if (result.finished && !result.error) {
        // CloudFront CDN에서 3D 모델 URL 생성
        const placements = await Promise.all(
            result.placements.map(async (placement) => ({
                ...placement,
                modelUrl: await cloudFrontService.getModelUrl(placement.furnitureType)
            }))
        );
        
        res.json({ finished: true, placements });
    } else {
        res.json({ finished: result.finished, error: result.error });
    }
});
```

### 3. 프론트엔드 (React Three Fiber)

3D 렌더링 및 배치 결과 표시:

```typescript
import { Canvas, useLoader } from '@react-three/fiber';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';

// API 서비스 훅
const useFurniturePlacement = () => {
    const requestPlacement = useCallback(async (request) => {
        const { jobId } = await fetch('/api/furniture/placement', {
            method: 'POST',
            body: JSON.stringify(request)
        }).then(res => res.json());
        
        // 결과 폴링
        return await pollForResult(jobId);
    }, []);
    
    return { requestPlacement };
};

// 가구 컴포넌트
const Furniture = ({ placement }) => {
    const { position, rotation, scale, modelUrl } = placement;
    const obj = useLoader(OBJLoader, modelUrl);

    // obj에 matrix 변환 적용
    
    return (
        <group
            position={[position.x, position.y, position.z]}
            rotation={[rotation.x * Math.PI / 180, rotation.y * Math.PI / 180, rotation.z * Math.PI / 180]}
            scale={[scale.x, scale.y, scale.z]}
        >
            <primitive object={obj} />
        </group>
    );
};

// 메인 컴포넌트
const FurniturePlacementApp = () => {
    
    ...

    return (
        <Canvas camera={{ position: [5, 5, 5] }}>
            <ambientLight intensity={0.5} />
            <OrbitControls />
            {placements.map(placement => (
                <Furniture key={placement.placementId} placement={placement} />
            ))}
        </Canvas>
    );
};
```

## 핵심 기술 요소

### 벡터 연산
3D 공간에서의 위치와 방향 계산:
```javascript
const calculateDistance = (pos1, pos2) => {
    const vector = new THREE.Vector3();
    vector.subVectors(pos2, pos1);
    return vector.length();
};
```

### 행렬 변환
아핀 변환을 통한 3D 변환 처리:
```javascript
const createTransformationMatrix = (position, rotation, scale) => {
    const matrix = new THREE.Matrix4();
    matrix.compose(position, new THREE.Quaternion().setFromEuler(rotation), scale);
    return matrix;
};
```

### CloudFront CDN
3D 모델 파일의 효율적인 배포:
```typescript
class CloudFrontModelManager {
    async getModelUrl(modelId: string): Promise<string> {
        return `https://${this.cloudFrontDomain}/models/${modelId}.obj`;
    }
    
    async uploadModel(modelId: string, modelFile: Buffer): Promise<string> {
        await this.s3Client.upload({
            Bucket: this.bucketName,
            Key: `models/${modelId}.obj`,
            Body: modelFile,
            CacheControl: 'public, max-age=31536000'
        }).promise();
        
        return this.getModelUrl(modelId);
    }
}
```

## 성능 최적화

### 아키텍처 기반 최적화

1. **분산 처리**: 쿠버네티스 포드 엔진에서 도형 연산을 독립적으로 처리
2. **비동기 통신**: FastAPI를 통한 비동기 작업으로 응답성 향상
3. **직접 콘텐츠 전달**: React 프론트엔드가 S3(CloudFront CDN)에서 직접 3D 모델 로딩

### 네트워크 최적화

- **메타데이터만 전송**: 위치, 회전, 스케일 정보만 전송하여 네트워크 부하 최소화
- **CloudFront CDN**: 전 세계 엣지 로케이션을 통한 빠른 모델 로딩
- **캐싱 전략**: 글로벌 캐싱과 브라우저 로컬 캐싱 활용

## 결론

이 시스템을 통해 다음과 같은 이점을 얻을 수 있습니다:

1. **효율적인 리소스 사용**: 3D 모델을 직접 스트리밍하지 않아 네트워크 부하 감소
2. **확장 가능한 아키텍처**: 쿠버네티스를 통한 엔진 스케일링
3. **정확한 도형 연산**: 벡터와 행렬 연산을 통한 정밀한 위치 계산
4. **실시간 렌더링**: React Three Fiber를 통한 부드러운 3D 렌더링

이러한 접근 방식을 통해 대용량 3D 데이터를 효율적으로 처리하면서도 사용자에게 풍부한 3D 경험을 제공할 수 있습니다.
