---
layout: post
title: "React Three Fiber의 스크린샷에서도 useEffect는 필요합니다."
# thumbnail: /assets/images/zone-subdivision-with-llm/Flowchart.png
categories: [three.js, react]
tags: [react-three-fiber, useEffect, screenshot, performance]  # red, yellow
# description: "React Three Fiber에서 스크린샷 기능을 구현할 때 useEffect를 사용하여 성능 최적화하는 방법"
featured: false
hidden: false
# rating: 4.5
# beforetoc: "React Three Fiber에서 스크린샷 기능 구현 시 주의사항"
# toc: true
---

## 요약
- React Three Fiber에서 스크린샷 기능을 구현할 때, 렌더링시 실행하는 것만 생각하고 추가하면 컴포넌트가 리렌더링될 때마다 스크린샷이 중복 실행될 수 있습니다. 이는 부모 컴포넌트의 상태 변경, Context 값 변화, Props 변경 등 다양한 이유로 발생하는 리렌더링 때문입니다. 
- 실제 개발 중에는 스크린샷 버튼을 한 번 클릭했는데 6번의 캡처가 실행되는 문제를 겪었습니다. 이를 해결하기 위해 `useEffect`를 사용하여 컴포넌트 마운트 시에만 스크린샷을 캡처하도록 변경했습니다.
- 결과적으로 스크린샷 캡처가 6번에서 1번으로 줄어들어 83%의 성능 향상을 달성할 수 있었습니다. 특히 3D 렌더링과 같은 무거운 작업에서는 이러한 최적화가 사용자 경험에 큰 영향을 미칩니다.

## 문제 상황

React Three Fiber에서 스크린샷 기능을 구현할 때, 다음과 같은 코드를 작성하는 경우가 있습니다:

```tsx
// ScreenShot.tsx - 문제가 될 수 있는 구현
import { useThree } from "@react-three/fiber";

interface ScreenShotProps {
  onImageExport?: (dataURL: string) => void;
}

export default function ScreenShot({ onImageExport }: ScreenShotProps) {
  const { gl, camera, scene } = useThree();
  
  // ❌ 컴포넌트가 렌더링될 때마다 실행됨
  gl.render(scene, camera);
  if (typeof onImageExport === 'function') {
    onImageExport(gl.domElement.toDataURL());
  }
  
  return null;
}
```

```tsx
// Premium.tsx - Canvas 내부에서 조건부 렌더링
<Canvas>
  {/* 3D 씬 내용들 */}
   ...
  {/* 위에 컴포넌트 생성이 끝난 후 캡쳐는 마지막에 */}
  <ScreenShot onImageExport={onImageExport} />
</Canvas>
```

## 왜 문제가 되는가?

React 컴포넌트는 다양한 이유로 여러 번 렌더링될 수 있습니다:

1. **부모 컴포넌트의 state 변경**
2. **Context 값의 변화**
3. **Props 변경**
4. **React의 Strict Mode (개발 환경)**
5. **상태 업데이트로 인한 리렌더링**

이러한 상황에서 조건부 렌더링만 사용하면, 컴포넌트가 재생성될 때마다 스크린샷이 여러 번 캡처될 수 있습니다.

### 실제 경험담: 6번 → 1번으로 개선

개발 중 실제로 겪은 문제입니다. `useEffect` 없이 조건부 렌더링만 사용했을 때:

```tsx
// ❌ 문제가 있던 코드
<ScreenShot onImageExport={onImageExport} />
```

이 코드로 스크린샷 버튼을 한 번 클릭했는데, **실제로는 6번의 캡처가 실행**되었습니다! 

이는 다음과 같은 이유 때문이었습니다:
- 부모 컴포넌트의 상태 변경으로 인한 리렌더링
- Canvas 내부의 다른 3D 객체들의 상태 변화
- React의 개발 모드에서의 이중 렌더링

`useEffect`를 적용한 후에는 **정확히 1번만 캡처**가 실행되어 성능이 크게 개선되었습니다.

## useEffect를 사용한 해결책

### 기본적인 해결 방법

```tsx
// ScreenShot.tsx - 개선된 구현
import { useEffect } from "react";
import { useThree } from "@react-three/fiber";

interface ScreenShotProps {
  onImageExport: (dataURL: string) => void;
}

export default function ScreenShot({ onImageExport }: ScreenShotProps) {
  const { gl, camera, scene } = useThree();

  useEffect(() => {
    // ✅ 컴포넌트가 마운트될 때 한 번만 실행
    const captureScreenshot = () => {
      try {
        gl.render(scene, camera);
        const dataURL = gl.domElement.toDataURL('image/png');
        onImageExport(dataURL);
      } catch (error) {
        console.error('스크린샷 캡처 실패:', error);
      }
    };

    captureScreenshot();
  }, [gl, camera, scene, onImageExport]);

  return null;
}
```

### 더 안전한 구현 (의존성 배열 최적화)

```tsx
// ScreenShot.tsx - 의존성 배열을 통한 최적화
import { useEffect } from "react";
import { useThree } from "@react-three/fiber";

interface ScreenShotProps {
  onImageExport: (dataURL: string) => void;
}

export default function ScreenShot({ onImageExport }: ScreenShotProps) {
  const { gl, camera, scene } = useThree();

  useEffect(() => {
    // ✅ 컴포넌트가 마운트될 때 한 번만 실행
    try {
      gl.render(scene, camera);
      const dataURL = gl.domElement.toDataURL('image/png');
      onImageExport(dataURL);
    } catch (error) {
      console.error('스크린샷 캡처 실패:', error);
    }
  }, []); // 빈 의존성 배열로 마운트 시에만 실행
  
  return null;
}
```

## 실제 사용 시나리오

### 다양한 스크린샷 요구사항

실제 프로젝트에서는 단순한 스크린샷 외에도 다양한 요구사항이 있을 수 있습니다:

```tsx
// 다양한 스크린샷 옵션을 지원하는 컴포넌트
import React, { useEffect } from "react";
import { useThree } from "@react-three/fiber";

interface ScreenShotProps {
  onImageExport: (dataURL: string) => void;
  options?: {
    format?: 'png' | 'jpeg';
    quality?: number;
    includeUI?: boolean;
  };
}

export default function ScreenShot({ onImageExport, options = {} }: ScreenShotProps) {
  const { gl, camera, scene } = useThree();

  useEffect(() => {
    try {
      gl.render(scene, camera);
      
      const { format = 'png', quality = 1.0 } = options;
      const dataURL = gl.domElement.toDataURL(`image/${format}`, quality);
      
      onImageExport(dataURL);
    } catch (error) {
      console.error('스크린샷 캡처 실패:', error);
    }
  }, []); // 컴포넌트 마운트 시에만 실행

  return null;
}
```

### 비동기 처리가 필요한 경우

```tsx
// 비동기 처리가 필요한 스크린샷
export function AsyncScreenShot({ onImageExport }: ScreenShotProps) {
  const { gl, camera, scene } = useThree();

  useEffect(() => {
    const captureWithDelay = async () => {
      try {
        // 렌더링 완료를 기다림
        await new Promise(resolve => setTimeout(resolve, 100));
        
        gl.render(scene, camera);
        const dataURL = gl.domElement.toDataURL();
        
        onImageExport(dataURL);
      } catch (error) {
        console.error('비동기 스크린샷 캡처 실패:', error);
      }
    };

    captureWithDelay();
  }, []);

  return null;
}
```

## useEffect가 해결하는 문제들

### 1. **불필요한 중복 실행 방지**
```tsx
// ❌ 컴포넌트가 리렌더링될 때마다 실행될 수 있음
if (condition) {
  expensiveOperation();
}

// ✅ 조건이 변경될 때만 실행됨
useEffect(() => {
  if (condition) {
    expensiveOperation();
  }
}, [condition]);
```

### 2. **성능 최적화**
스크린샷 캡처는 CPU 집약적인 작업입니다. `useEffect`를 사용하면:
- 필요한 시점에만 실행
- 불필요한 중복 실행 방지
- 메모리 누수 방지

### 3. **예측 가능한 동작**
컴포넌트의 렌더링과 부수 효과를 분리하여 예측 가능한 동작을 보장합니다.

## 주의사항

### 1. **의존성 배열 관리**
```tsx
// ✅ 스크린샷은 한 번만 캡처하면 되므로 빈 배열 사용
useEffect(() => {
  captureScreenshot();
}, []); // 컴포넌트 마운트 시에만 실행

// ❌ 불필요한 의존성으로 인한 중복 실행
useEffect(() => {
  captureScreenshot();
}, [gl, camera, scene, onImageExport]); // 의존성이 변경될 때마다 실행됨
```

### 2. **클린업 함수 사용**
```tsx
useEffect(() => {
  const timeoutId = setTimeout(() => {
    captureScreenshot();
  }, 100);

  return () => clearTimeout(timeoutId); // 클린업
}, [dependencies]);
```

## 결론

React Three Fiber에서 스크린샷과 같은 부수 효과(side effect)를 다룰 때는 반드시 `useEffect`를 사용해야 합니다. 

### 실제 성능 개선 결과
- **Before**: 스크린샷 버튼 1회 클릭 → 6번 캡처 실행
- **After**: 스크린샷 버튼 1회 클릭 → 1번 캡처 실행
- **개선율**: **83% 성능 향상** (6번 → 1번)

### useEffect 사용의 장점
- **성능 최적화**: 불필요한 중복 실행 방지
- **예측 가능성**: 컴포넌트 리렌더링과 독립적인 실행
- **메모리 관리**: 적절한 클린업으로 메모리 누수 방지
- **디버깅 용이성**: 부수 효과의 실행 시점을 명확히 파악 가능

특히 3D 렌더링과 같은 무거운 작업에서는 이러한 최적화가 사용자 경험에 큰 영향을 미칩니다. 실제로 스크린샷 캡처 시간이 6배 단축되어 사용자가 체감할 수 있는 성능 향상을 경험할 수 있었습니다.

