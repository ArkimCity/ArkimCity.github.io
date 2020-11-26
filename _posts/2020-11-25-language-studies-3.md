---
title: "Language Study - SQL - 3. 내가 보려고 만든 테이블 생성 및 조작"
date: 2020-11-25
categories: LanguageStudies
tags: SQL
languages: SQL
---

테이블 생성 및 조작 연습



stulist 테이블 생성 
```sql
drop table stulist;

create table stulist(
	id number(3) constraint stulist_empno_pk primary key,
	name varchar2(20),
    score number(3) not null, 
    plagiarism number(3),
    grade varchar2(20)
);
```

stulist 데이터 삽입
```sql
insert all
	into stulist(id, name, score, plagiarism) values(1, '김재웅', 75, 90)
	into stulist(id, name, score, plagiarism) values(2, '이정민', 68, 10)
	into stulist(id, name, score, plagiarism) values(3, '이민재', 99, 60)
	into stulist(id, name, score, plagiarism) values(4, '염아정', 84, 40)
	into stulist(id, name, score, plagiarism) values(5, '최지원', 70, 20)
	into stulist(id, name, score, plagiarism) values(6, '최지수', 90, 80)
    into stulist(id, name, score, plagiarism) values(7, '권희성', 48, 10)
select * from dual;

select * from stulist;
```



-- cash 테이블 생성 
```sql
drop table cash;

create table cash(
	id number(3) constraint cash_id_fk references stulist,
	money varchar2(20),
    plus number(3) 
);
```

-- cash 테이블에 데이터 삽입
```sql
insert all
	into cash(id, money, plus) values(1, 'TRUE', 20)
    into cash(id, money, plus) values(2, 'TRUE', 20)
    into cash(id, money, plus) values(3, 'TRUE', 20)
    into cash(id, money) values(4, 'FALSE')
    into cash(id, money, plus) values(5, 'FALSE', 0)
    into cash(id, money, plus) values(6, 'FALSE', 0)
select * from dual;

select * from cash;
```



-- grades 테이블 생성 및 데이터 삽입
```sql
drop table grades;

create table grades(
    grade varchar2(2),
    minscore number(3),
    maxscore number(3)
);

insert into grades(grade, minscore , maxscore) values('A', 90, 200);
insert into grades(grade, minscore , maxscore) values('B', 70, 89);
insert into grades(grade, minscore , maxscore) values('C', 50, 69);
insert into grades(grade, minscore , maxscore) values('D', 0, 49);

select * from grades order by grade asc;
```



--plagiarisms 테이블 생성 및 데이터 삽입
```sql
drop table plagiarisms;

CREATE table plagiarisms(
    penalty number(3), 
    minp number(3), 
    maxp number(3)
);

INSERT INTO plagiarisms(penalty, minp, maxp) values(-50 , 90, 200);
INSERT INTO plagiarisms(penalty, minp, maxp) values(20 , 70, 89);
INSERT INTO plagiarisms(penalty, minp, maxp) values(0 , 0, 69);

SELECT *
FROM plagiarisms
ORDER BY maxp ASC;
```



--Q1.alt stulist랑 cash 테이블만 사용해 점수를 계산해서 점수를 출력해보시오.

--A1.
```sql
select s.SCORE + nvl(c.PLUS,0)
from stulist s, cash c
where s.ID=c.ID(+);
```


--Q2. stulist, cash, plagiarisms 테이블을 사용해서 총점을 계산하고 등급을 도출해서 (id, 이름, 최종점수, grade) 를 출력해보시오.

--A2.
```sql
select id, name, score2, grade
from 
(select s.SCORE + nvl(c.PLUS,0) + penalty as score2, name, s.id
from stulist s, cash c, plagiarisms p
where s.ID=c.ID(+) and s.plagiarism between p.minp and p.maxp
), grades
where score2 between minscore and maxscore;
```