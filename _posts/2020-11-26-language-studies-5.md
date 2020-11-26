---
title: "Language Study - SQL - 5. 내가 보려고 만든 view, rownum(ORACLE DB)"
date: 2020-11-26
categories: LanguageStudies
tags: SQL
languages: SQL
---
1. view

기본 문법

```sql
drop view dep01_v;

create view dep01_v as select * from dept01;
```

view를 수정하면 끌어다 쓴 원본 데이터도 변경됨


합쳐서 쓰는걸 자주 보는데, 이걸 뷰로 만들어놓고 보는것도 가능
```sql
drop view empdept_v;

create view empdept_v as (select empno, ename, emp01.deptno, loc
from emp01, dept01
where emp01.deptno=dept01.deptno);
```

2. rownum

```sql
select rownum, deptno
from dept
where rownum=1
order by deptno desc;
```
이렇게 쓰면 당연하다는 듯이 결과가 나오지만,

```sql
select rownum, deptno
from dept
where rownum=2
order by deptno desc;
```
이렇게 쓰는 순간 결과가 출력되지 않는다.

몇가지를 해보자
```sql
select rownum, deptno
from dept
where rownum<=2
order by deptno desc;
```
나온다
```sql
select rownum, deptno
from dept
where rownum>=2
order by deptno desc;
```
안나온다.

원리에 대한 설명 전에 해결책을 간단히 보자면

```sql
select rownum, deptno
from (select rownum, deptno
		from dept)
where rownum=2;
```
rownum을 다른 이름으로 맵핑해주니 성공

```sql
select rownum, deptno
from (select rownum, deptno
	from dept)
where rownum>2;
```
이렇게 할 경우 다시 결과가 나오지 않음.

왜냐하면 rownum을 선택했다고 하더라도 다시 마지막에 rownum을 붙이면 이 때의 rownum은 안에서 불러다 쓴게 아니라 다시 바깥에서 새로 rownum을 실행한 효과가 나온다.

```sql
select rownum, rn, deptno
from (select rownum as rn, deptno
	from dept)
where rn>2;
```
이렇게 될 경우 
두가지 시사점이 있다.
	1. as를 통해 지정해줄 경우 바깥에서 불러오는 rownum이 아닌 여기서처럼 지정해둔 rn을 사용할 수 있다. 즉 as를 통해 지정하면 별도의 데이터셋이 생긴것과 같은 효과가 생긴다.
	
	2. rownum을 사용한다는 것은 rownum의 조건이 반복적으로 실행되고 실행된 다음 결과가 이전 결과가 같을 때까지 계속 실행된다.
	ex) rownum > 2 와 같은 조건은 반복실행될 경우 결국 rownum=1 이 계속 버려지고, 아무것도 남지 않는다.

* 추가 시사점 - thanks to 최태열(https://ta-ye.github.io/)

```sql
select rownum, deptno
from dept
order by deptno desc;
```
```sql
select rownum, deptno
from dept
order by deptno asc;
```

숫자로 정렬하면 문제없이 rownum이 1부터 나오게 되는데,

```sql
select rownum, dname
from dept
order by dname desc;
```
```sql
select rownum, dname
from dept
order by dname asc;
```

문자로 정렬하니 rownum이 엉킨다!

```sql
select rownum, empno
from emp
order by empno asc;
```
```sql
select rownum, sal
from sal
order by empno asc;
```
현재 이해한 바로는 primary key가 세팅이 되어있을 경우 이 칼럼을 기준으로 해서 그렇다.

sal가 숫자인데도 이렇게 나오고, empno가 primary key인데 잘 나온다.