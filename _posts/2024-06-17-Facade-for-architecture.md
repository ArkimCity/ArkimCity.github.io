---
layout: post
title:  "Facade for Architectural Element"
# author: john
categories: [ Automation ]
tags: []  # red, yellow
# image: assets/images/11.jpg
description: "설계 자동화에 필요한 코드 전략 - 파사드 패턴"
featured: false
hidden: false
# rating: 4.5
beforetoc: "test"
toc: false
---


```python
class Builder:
    def __init__(self, site_geom):
        self.site_geom = site_geom
        self.building = Building(self)
        self.axis = Axis(self)

    def generate_axis_candidates(self):
        self.axis.generate_candidates()

class Building:
    def __init__(self, builder):
        self.builder = builder
        self.core = Core(self)
        self.stories = [Story(self) for _ in range(5)]  # 예를 들어 5층 건물

class Axis:
    def __init__(self, builder):
        self.builder = builder

    def generate_candidates(self):
        self.builder =
        # site_geom을 기반으로 축 후보군을 생성하는 로직 구현
        print("Generating axis candidates based on site geometry.")

class Core:
    def __init__(self, building):
        self.building = building

class Story:
    def __init__(self, building):
        self.building = building
```
