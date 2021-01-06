---
title: "Language Study - TypeScript - 3. 함수"
date: 2020-12-10
categories: LanguageStudies
tags: TypeScript javascript
languages: TypeScript
---


## 1. 함수의 타입

함수를 사용하기 위해서는 매개변수의 타입과 반환하는 반환값의 타입이 필요하고, 기본 표현은 다음과 같다.

```typescript
function sum(a: number, b: number): number {
  return (a + b);
}
```

괄호 안에 들어가는 첫번째와 두번째 number가 변수용, 마지막 number가 반환값 용 타입 선언이 된다.

리턴이 undefined, null 등의 경우 void를 사용한다. 

```typescript
function print(a: number): void {
  console.log(a);
}
```

