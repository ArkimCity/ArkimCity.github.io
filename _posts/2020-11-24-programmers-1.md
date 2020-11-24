---
title: "Programmers Practice 1"
date: 2020-11-24
categories: CodingTest
tags: programmers java
languages: java
---
programmers - 비밀지도

Question-url : https://programmers.co.kr/learn/courses/30/lessons/17681

2진법을 만드는 부분의 의미가 있다고 생각해 아카이빙 해둡니다.

```java
import java.util.ArrayList;

class Solution {
	public static String[] solution(int n, int[] arr1, int[] arr2) {
		String[] answer = new String[n];
		ArrayList<String> list1 = new ArrayList<String>(n);

		for (int i : arr1) {
			String l1 = new String();
			for (int j = n - 1; j >= 0; j = j - 1) {
				if (Math.pow(2, j) <= i) {
					i = (int) (i - Math.pow(2, j));
					l1 = l1 + "#";
				} else {
					l1 = l1 + " ";
				}
			}
			list1.add(l1);
		}
		ArrayList<String> list2 = new ArrayList<String>(n);

		for (int i : arr2) {
			String l2 = new String();
			for (int j = n - 1; j >= 0; j = j - 1) {
				if (Math.pow(2, j) <= i) {
					i = (int) (i - Math.pow(2, j));
					l2 = l2 + "#";
				} else {
					l2 = l2 + " ";
				}
			}
			list2.add(l2);
		}
		for (int k = 0; k < n; k++) {
			String anspart = "";
			for (int l = 0; l < n; l++) {
				if (list1.get(k).charAt(l) == '#' || list2.get(k).charAt(l) == '#') {
					anspart += "#";
				} else {
					anspart += " ";
				}
			}
			answer[k] = anspart;
		}
		return answer;
	}
}
```

