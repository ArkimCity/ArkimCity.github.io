---
title: "Language Study - SQL - 2. 내가 보려고 만든 기본 문법 정리 1"
date: 2020-11-24
categories: LanguageStudies
tags: SQL
languages: SQL
---

*기본환경은 SCOTT 파일을 이용합니다.

```sql
set linesize 200
set pagesize 200
```
사이즈 조절

```sql
select * 
from emp;
```
최초 기본형

```sql
select * 
from emp
where ename='SMITH';
```
기본 조건절

```sql
select * 
from emp
order by sal desc;
```
정렬

```sql
select distinct deptno
from emp
order by deptno asc;
```
distinct를 통한 중복 제거

```sql
select ename, sal*12+comm 
from emp;
```
계산도 가능

```sql
select ename, sal*12+nvl(comm,0) 
from emp;
```
null값이 연산에 섞이면 결과가 안나오니 0으로 변환

```sql
select ename, job 
from emp 
where deptno = 10
order by ename asc;
```
order by는 where 뒤에 붙는다 

```sql
select ename, job 
from emp 
where deptno = 10 or job = 'MANAGER' 
order by ename asc;
```
or and도 사용이 가능

```sql
select ename, job 
from emp 
where deptno in (10,20) and deptno is not null;
```
in, is, not, null을 통해 사용 가능

```sql
select ename, job 
from emp 
where deptno != 10 and sal >= 3000;
```
같지 않다와 크기 비교 사용 가능

```sql
select ename, hiredate 
from emp 
where hiredate between '81/01/01' and '81/12/31';
```
사이에 있는 값 할 수 있는데 날짜도 가능

```sql
select ename, hiredate 
from emp 
where ename like '___M' or ename like '%M' or ename like '_M___' or ename like '%M%';
```
비슷한 거 출력 가능 _을 사용할떄는 글자수 정확히 필요