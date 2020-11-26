---
title: "Language Study - SQL - 4. 내가 보려고 만든 integrity(ORACLE DB)"
date: 2020-11-26
categories: LanguageStudies
tags: SQL
languages: SQL
---

제약 사항 생성 및 삽입 연습

대표 제약 사항

```SQL
	TABLE_NAME                                                   CO
	------------------------------------------------------------ --
	CONSTRAINT_NAME
	------------------------------------------------------------
	DEPT                                                         P
	PK_DEPT

	EMP                                                          P
	PK_EMP

	EMP                                                          R
	FK_DEPTNO

	EMP02                                                        C
	SYS_C007023

	EMP02                                                        P
	EMP02_EMPNO_PK

	EMP02                                                        R
	EMP02_DEPTNO_FK
```

p : pk 의미
r : fk 의미 (references)
c : 이름 미 부여시. 보통 not null 의미

