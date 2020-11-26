---
title: "Language Study - SQL - 4. 내가 보려고 만든 integrity(ORACLE DB)"
date: 2020-11-26
categories: LanguageStudies
tags: SQL
languages: SQL
---

제약 사항 생성 및 삽입 연습

대표 제약 사항
p : pk 의미- unique + not null과 같은 효과
r : fk 의미 (references)
c : 이름 미 부여시. 보통 not null 의미

+ unique - 이름 그대로 중복 불가
+ check - where와 비슷하게 사용하고 싶을 경우 사용
```sql
drop table emp03;

create table emp03(
	empno number(3) constraint emp03_empno_c check (empno between 1 and 100),
    num number(3) constraint emp03_empno_u unique
);
```
+ default - insert 시에 데이터 없어도 알아서 들어가있는거 (자바에서 기본 생성자 생성시 변수 지정하는거 같은거임)

이름은 지정해줄 수 있다.

```sql
	TABLE_NAME                      CO
	----------------------------- -----
	CONSTRAINT_NAME
	---------------------------
	DEPT                            P
	PK_DEPT

	EMP                             P
	PK_EMP

	EMP                             R
	FK_DEPTNO

	EMP02                           C
	SYS_C007023

	EMP02                           P
	EMP02_EMPNO_PK

	EMP02                           R
	EMP02_DEPTNO_FK
```

제약 조건 선언 방법

1. 이름 지정
2. 위치
3. 추후 삽입

1. 이름 지정

```sql
drop table emp02;

create table emp02(
	empno number(4),
	ename varchar2(20) not null
    deptno number(2),
    constraint emp02_empno_pk primary key (empno),
    constraint emp02_deptno_fk foreign key (deptno) references dept(deptno)
);
```

```sql
drop table emp02;

create table emp02(
	empno number(4) constraint stulist_empno_pk primary key,
	ename varchar2(20) not null
    deptno number(2) constraint emp02_deptno_fk references dept(deptno)
);
```


2. 위치

```sql
drop table emp02;

create table emp02(
	empno number(4) primary key,
	ename varchar2(20) not null
);
```


```sql
drop table emp02;

create table emp02(
	empno number(4),
	ename varchar2(20) not null, 
	constraint emp02_empno_pk primary key (empno)
    gender varchar2(10) constraint emp01_gender_c check (gender='M' or gender='F')
);
```

3. 추후 삽입

```sql
alter table emp01 add constraint emp01_deptno_fk foreign key (deptno) references dept01(deptno);
```