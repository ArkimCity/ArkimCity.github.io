---
title: "Language Study - TypeScript - 2. 기본 문법 - 2"
date: 2020-12-09
categories: LanguageStudies
tags: TypeScript javascript
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

## 2. 객체 생성

객체 생성에 대한 기본 표현은 다음과 같다.
```typescript
const user: {
     name: string; 
     age: number; 
} = { 
    name: '김재웅', 
    age: 27 
};
```

?를 통해 값이 없어도 가능한 속성으로 만든다. (선택 속성)

```typescript
const userWithUnknownHeight: {
    name: string; 
    age?: number; 
} = { 
  name: '김재웅' 
};
```

readonly를 통해 읽기 전용으로 만든다.

```typescript
const user: { 
    readonly name: string; 
    height: numer; 
} = { 
    name: '김재웅', 
    age: 27 
};

// user.name = 'Jaeung Kim';
//변경불가 에러
```

## 3. 별칭

타입은 별칭을 통한 사용도 가능하다. 이때 별도의 타입이 생긴 것이 아니고, 이름만 빌려서 사용한 것이다. 

```typescript
type StringTypeNickName = string;
type NumberTypeNickName = number;
```

심지어 여러개 타입을 합쳐 하나의 타입으로 사용이 가능할 때도 사용할 수 있다.

```typescript
type User = {
  name: string;
  age: number;
};
```