---
title: "Language Study - TypeScript - 1. 기본 문법 - 1"
date: 2020-11-30
categories: LanguageStudies
tags: TypeScript
languages: TypeScript
---
## 1. 의의

javascript의 중요성은 이제와서 말할 필요도 없다. 다만 자바스크립트의 동적 타입 객체 이용이 가져다주는 장기 개발에 불리한 특성을 보완해 자바스크립트에 타입을 더해 코드 소통 및 개발에 편리를 더할 수 있다.

-VSC를 사용중이신 분은 npm install typescript 를 터미널에 한번 치고 시작하세요! 컴파일러가 설치됩니다.-


## 2. 자바스크립트와 아주 간단한 비교
먼저 자바 스크립트를 보고 가자
```javascript
var words1 = "hello world!";
let words2 = "hello world!";
const words2 = "hello world!";
```
위와 같은 자바스크립트 선언 3가지를 써볼 수 있다. 세개의 차이점은 잘 설명해 놓은 곳이 많아서 여기서는 일단 'const words2 = "hello world!';'를 예로 들어볼까 한다.

```typescript
const words: string = "hello world!";
```
가장 큰 차이점이 바로 드러난다. 자바에서 
```java
String words = "hello world!";
```
라고 한 것 마냥 string이라 명시해주는 것이다. 


## 3. 기본 타입들
마찬가지로
```typescript
const numbers: number = 100;
```
와 같이 number 타입(자바 스크립트 에서는 정수를 따로 구분하지 않는다고 한다)

```typescript
const isTrue: boolean = true;
const nullValue: null = null;
const undefinedValue: undefined = undefined;
```
와 같은 타입도 존재한다.

```typescript
var anything: any = "Really Anything?";
var anything: any = 5252;
var anything: any = true;
```
타입에 구애받지 않는 객체를 정 만들어야 할 땐 any 타입을 사용한다.

```typescript
function nothing(): void { }
```
java 생성자의 void와 비슷하게 이해하면 된다.

```typescript
var notever: never;

function noteverfunction(): never {
    throw new Error(``);
  }
```
값을 넣을 수 없는 never 와 같은같은 별난 타입도 존재한다.


## 4. 정리
나 역시도 그렇지만 동적타입 객체를 사용하는 파이썬이나 자바스크립트로 코딩을 입문하는 사람이 많을텐데(전 파이썬) 실제 정해진 타입을 계산 혹은 개발 과정에서 변경하는 경우는 거의 없을 뿐더러 , 악명높은 소문을 가진 포인터의 c까진 아니더라도 자바를 할 때 타입 선언에 적응하기 시간이 걸리는 경우가 많다. 

자바 스크립트에서 type 선언하는 습관을 들여놓으면 추후 개발에 있어서도 원활한 소통과 명확한 이해가 동반됨이 기대되기에 처음에 길을 잘 들여놓을까 한다.