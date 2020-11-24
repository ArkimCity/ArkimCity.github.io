---
title: "Language Study - SQL - 1. Outer Join에 관하여"
date: 2020-11-24
categories: LanguageStudies
tags: SQL
languages: SQL
---

*기본환경은 hr파일을 이용합니다.

```sql
select * 
from employees;
```

```sql
select * 
from departments;
```

이 두 결과값을 단순히 합쳐버리면 

```sql
select * 
from employees, departments;
```

양쪽의 수를 곱한 엄청 큰 경우의 수가 튀어나온다. 따라서 둘을 합치는 기준이 필요하다.

한 파일 내의 두 테이블은 department_id 를 공유한다. 이 공유하는 id를 이용해서 양쪽의 테이블을 합쳐서 보여주는 기준으로 사용한다.

```sql
select * 
from employees, departments
where employees.department_id=departments.department_id;
```

일반적으로는 이렇게 합치는 것이 타당하다.
하지만 대부분의 경우 두 테이블을 합치는 과정에서 누락 혹은 오류가 생길 가능성이 농후하다.
결과는 106 rows가 나온다.

먼저 null이 어떤 row인지 확인해보자

```sql
select first_name
from employees
where department_id is null;
```

Kimberely

값이 나왔다.

실제로 employees는 107 rows를 가지고 있다. 이는 양쪽의 department_id를 비교하는 과정에서 department_id가 누락된 row가 무시된 것이다.

이 경우 (+) 를 사용한다.

```sql
select * 
from employees, departments
where employees.department_id=departments.department_id(+);
```
```sql
select * 
from employees, departments
where employees.department_id(+)=departments.department_id;
```
이때 (+)의 위치가 매우 혼란스러운데, 결론적으로 얘기하자면 온전히 출력하고 싶은 쪽의 반대편에 붙혀준다.

현재 상황은 모든 employees를 출력하는 목적을 가지고 있다고 하자.

아까 결과로 나왔던 Kimberely를 이용해보자

```sql
select first_name 
from employees, departments
where employees.department_id(+)=departments.department_id and first_name='Kimberely';
```
```sql
select first_name 
from employees, departments
where employees.department_id=departments.department_id(+) and first_name='Kimberely';
```

결과적으로 위의 결과는 no rows

아래에서는 이름이 출력되었다.

아까 언급한 온전히 출력하고 싶은 쪽의 반대편이란 말은 다음과 같다.

```sql
where employees.department_id=departments.department_id(+)
```

의 경우 emplyees의 department_id가 존재하는 경우 departments 의 department_id를 이용해 값을 할당해주고 할당해줄 수 없는 것들은 그냥 할당하지 않은채 출력이 된다.

```sql
where employees.department_id(+)=departments.department_id
```
의 경우 반대로 departments 가 가진 department_id가 모두 출력되는 걸 보장한채 서로 같은 게 할당이 되며 출력된다. 특히 비교대상인 department_id는 물론, +의 반대쪽인 쪽은 모든 정보를 가지고 온다.

----------------------------------
정리하자면 다음과 같다.

outer join 과정에서 두 표가 서로 같은 부분은 합쳐주고,
(+)를 붙이는 쪽에 가상의 공간을 만들어 반대쪽 표를 온전히 지킬 수 있게 된다.



*사진을 모두 첨부할 수 없으니 이 글을 보신 뒤에 헷갈린다면 꼭 해보시는 걸 추천합니다.

