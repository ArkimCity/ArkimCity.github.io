---
title: "Language Study - TypeScript - 2. 입문 - 2"
date: 2020-12-09
categories: LanguageStudies
tags: TypeScript
languages: TypeScript
---


## 1. 배열 및 tuple 선언

기본 배열 타입은 다음과 같이 표현한다.

```typescript
const numbers: number[] = [0,1,1,2,1];
const strings: string[] = ['one', 'two', 'three'];
```

다음과 같이 표현할 수도 있다.

```typescript
const numbers: Array<number> = [0,1,1,2,1];
const strings: Array<string> = ['one', 'two', 'three'];
```

튜플 타입은 타입을 지정해서 변경 없이 저장하는 용도이기 때문인 경우가 많은데, 아예 다른 타입을 같이 선언할 수도 있다. 명시된 개수 만큼만 원소를 가질 수 있기 때문에, 아래와 같은 경우

```typescript
const stringandnumber: [string, number] = ['string', 123]
// const stringandnumber: [string, number] = ['string', 'string', 123] 
// 오류 발생
```
이 일어난다. (2.7 버전에서부터 이와 같이 적용되었다고 한다.)