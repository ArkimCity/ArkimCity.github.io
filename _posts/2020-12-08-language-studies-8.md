---
title: "Language Study - JPA - 1. 시작 및 기본 설정단계 - 1"
date: 2020-12-08
categories: LanguageStudies
tags: java JPA
languages: java
---

## 1. JPA

JPA는 jdbc와의 연동 확장, 최종적으로 oracledb 등의 SQL 형식의 DB를 효과적으로 이용하기 위한 툴의 일종으로 구조가 mybatis 등에 비해 다소 까다롭지만 장기사용성이 크게 뛰어나다. 실행 속도가 sql을 직접 이용하는 것에 비해 다소 느릴 수 있지만, 그 밖에 여러가지 장점이 많아 현업에서 사용이 늘어나는 추세이다.

자바 클래스를 entity 화 시키고 이를 Persistence Context라는 중간단계를 사용해 관리 및 sql 전송 등을 사용할 수 있는 방법이다. 그 영속성 컨텍스트에서 정보를 관리하고 나중에 한번에 sql로 전송하기때문에 commit 이 이루어지는 시점에 변경을 감지해 db에 전송한다. (즉 @Test에 있는 모든 문장을 부턱대고 db로 쏘는 것이 아니다.)

## 2. 시작

기본이 되는 xml파일을 들여다보면 다음과 같다. 익숙하게 바로 이해할 수 있는 클래스 부분과 오라클db 주소, 유저와 패스워드 이후에는

dialect - ex) 오라클 db를 사용할거다.
show - hibernate 과정을 콘솔에 보여준다.
format - 좀 정리해서
comments - 간단한 코멘트 및 설명

ddl.auto - 자동 테이블 drop 및 create 등의 내용으로 구성되어있다. 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
	<persistence-unit name="oracleDBUse">
		<class>step02.entity.Member</class>
		<class>step02.entity.Team</class>
		<properties>
			<property name="javax.persistence.jdbc.driver" value="oracle.jdbc.OracleDriver" />
			<property name="javax.persistence.jdbc.url" value="jdbc:oracle:thin:@127.0.0.1:1521:xe" />
			<property name="javax.persistence.jdbc.user" value="SCOTT" />
			<property name="javax.persistence.jdbc.password" value="TIGER" />

			<property name="hibernate.dialect" value="org.hibernate.dialect.OracleDialect" />
			<property name="hibernate.show_sql" value="true" />
			<property name="hibernate.format_sql" value="true" />
			<property name="hibernate.use_sql_comments" value="true" />
			
			<property name="hibernate.hbm2ddl.auto" value="create" />
		</properties>

	</persistence-unit>
</persistence>
```

## 3. 적용 1 - java class에서 persistence.xml 내용 불러오기

persistence-unit name을 oracleDBUse으로 설정해놓은 만큼, 이에 해당하는 EntityManagerFactory를 불러오는게 1순위이다. 이를 통해 EntityManager를 생성하며 return 시켜주는 것으로 작업 전반에 공통으로 사용될 부분을 만들어둔다.

```java
package util;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class PublicCommon {
	private static EntityManagerFactory emf;
	
	static {
		emf = Persistence.createEntityManagerFactory("oracleDBUse");
	}
	
	public static EntityManager getEntityManger() {
		return emf.createEntityManager();
	}

	public static void close() {
		emf.close();
	}
}
```

## 4. 적용 2 - DTO 클래스 만들기 (Team & Member 내용 포함)

먼저 기본 구조를 보여주는 클래스의 예시이다. 생략해도 되는 구문이 많지만 배우는 단계이니 만큼 최대한 적어놓고자 한다.

기본은 
@Id는 프라이머리 키에 해당하는 내용이고
@Column 이 sql 컬럼화 시키는 내용이다. 

```java
package step02.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

@Builder
@Entity
@SequenceGenerator(name = "team_seq_gen", sequenceName = "team_seq_id", initialValue = 1, allocationSize = 50)
public class Team {

	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "team_seq_gen")
	@Column(name = "team_id")
	private Long id;

	@Column(length = 20, name = "team_name")
	private String teamName;
}
```

짧게는 @GeneratedValue를 이용해 기본값을 이용해 db에서 사용할 시퀀스를 만들어줘도 되고 굳이 이름 지정할 필요가 없으면 지정하지 않아도 된다. (length조차 선택이다.)

```java
package step02.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

@Builder
@Entity
public class Team {

	@Id
	@GeneratedValue
	@Column(name = "team_id")
	private Long id;

	@Column(length = 20)
	private String teamName;
}
```

여기서 아래의 Member 클래스에 가장 중요한 건 

@OneToOne

@JoinColumn(name = "team_id") 

private Team teamId;

에 해당하는 내용인데, 앞서 설정한 Team 클래스의 "team_id"를 foreign key로 받아오기 위해 설정하는 것이다. 이때 String이나 Long이 아닌 Team, 즉 table에 해당하는 클래스를 받아서 사용해야 원활한 join이 이루어진다.

```java
package step02.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.SequenceGenerator;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

@Builder
@Entity
@SequenceGenerator(name = "member_seq_gen", sequenceName = "member_seq_id", initialValue = 1, allocationSize = 50)
public class Member {
	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "member_seq_gen")
	@Column(name = "member_id")
	private Long memberId;

	@Column(length = 20)
	private String name;

	private int age;

	@OneToOne
	@JoinColumn(name = "team_id")
	private Team teamId;

}
```


## 5. 실행

엔티티 매니저를 불러온 뒤에 트랜색션 객체를 생성해 비긴을 시켜준다.

try 안의 내용들이 sql 테이블로 보낼 내용들을 준비하는 객체 생성 단계가 되고, tx.commit();을 통해 적용시킨다. 

마지막에 em.close();를 통해 객체를 반환한다.

```java
package run.test;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;

import org.junit.jupiter.api.Test;

import step02.entity.Member;
import step02.entity.Team;
import util.PublicCommon;

public class RunningTest {
	
	@Test
	public void runningTest2() {
		EntityManager em = PublicCommon.getEntityManger();
		EntityTransaction tx = em.getTransaction();
		tx.begin();
		
		try {
			Team t1 = Team.builder().teamName("team A").build();
			em.persist(t1);
			Team t2 = Team.builder().teamName("team B").build();
			em.persist(t2);
	
			Member m1 = Member.builder().age(20).name("김재웅").teamId(t2).build();
			em.persist(m1);
			
			tx.commit();
		} finally {
			em.close();
		}
	}
}
```