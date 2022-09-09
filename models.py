# partially copied from https://github.com/das08/kuRakutanBot-go/blob/master/src/app/models/kuwiki/kuwiki.go


"""
go description:

package main

// This file was generated from JSON Schema using quicktype, do not modify it directly.

import "encoding/json"

func UnmarshalKUWiki(data []byte) (KUWiki, error) {
	var r KUWiki
	err := json.Unmarshal(data, &r)
	return r, err
}

func (r *KUWiki) Marshal() ([]byte, error) {
	return json.Marshal(r)
}

type KUWiki struct {
	Count    int64       `json:"count"`
	Next     interface{} `json:"next"`
	Previous interface{} `json:"previous"`
	Results  []Result    `json:"results"`
}

type Result struct {
	ID              int64        `json:"id"`
	CourseCode      string       `json:"course_code"`
	CourseNumbering string       `json:"course_numbering"`
	Name            string       `json:"name"`
	Field           string       `json:"field"`
	LectureSet      []LectureSet `json:"lecture_set"`
	ExamSet         []ExamSet    `json:"exam_set"`
	ExamCount       int64        `json:"exam_count"`
}

type ExamSet struct {
	CourseCode   string `json:"course_code"`
	Name         string `json:"name"`
	Field        string `json:"field"`
	DriveID      string `json:"drive_id"`
	DriveLink    string `json:"drive_link"`
	DriveLinkTag string `json:"drive_link_tag"`
}

type LectureSet struct {
	Year            int64  `json:"year"`
	GroupCode       string `json:"group_code"`
	Code            string `json:"code"`
	Name            string `json:"name"`
	InstructorSet   []Set  `json:"instructor_set"`
	PeriodSet       []Set  `json:"period_set"`
	Semester        string `json:"semester"`
	Major           string `json:"major"`
	URL             string `json:"url"`
	NumPeriods      int64  `json:"num_periods"`
	CourseCode      string `json:"course_code"`
	CourseNumbering string `json:"course_numbering"`
}

type Set struct {
	Lecture string `json:"lecture"`
	Name    string `json:"name"`
}
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional
import random
import hashlib

def rand_str(rand: random.Random, nbytes:int=10)->str:
	b = rand.randbytes(nbytes)
	return b.hex()

@dataclass_json
@dataclass
class Set:
	lecture:str
	name:str

@dataclass_json
@dataclass
class LectureSet:
	year:int
	group_code:str
	code:str
	name:str
	instructor_set:List[Set]
	period_set:List[Set]
	semester:str
	major:str
	url:str
	num_periods:int
	course_code:str
	course_numbering:str

	@classmethod
	def random(cls,seed:random.Random,lecture_name:str)->'LectureSet':
		return cls(
			year=seed.randint(2000,2020),
			group_code=rand_str(seed),
			code=rand_str(seed),
			name=lecture_name,
			instructor_set=[],
			period_set=[],
			semester=rand_str(seed),
			major=rand_str(seed),
			url=rand_str(seed),
			num_periods=seed.randint(1,10),
			course_code=rand_str(seed),
			course_numbering=rand_str(seed),
		)

@dataclass_json
@dataclass
class ExamSet:
	course_code: str
	name:str
	field:str
	drive_id:str
	drive_link:str
	drive_link_tag:str

	@classmethod
	def random(cls, seed:random.Random,lecture_name:str,field_name:str)->'ExamSet':
		return cls(
			course_code=rand_str(seed),
			name=lecture_name,
			field=field_name,
			drive_id=rand_str(seed),
			drive_link=rand_str(seed),
			drive_link_tag=rand_str(seed)
		)

@dataclass_json
@dataclass
class Result:
	id: int
	course_code: str
	course_numbering: str
	name: str
	field: str
	lecture_set: List[LectureSet]
	exam_set: List[ExamSet]
	exam_count: int

	@classmethod
	def random(cls,seed:random.Random,lecture_name:str)->'Result':
		course_code=rand_str(seed)
		field=rand_str(seed)
		lecture_count = seed.randint(1, 4)
		lecture_set = [LectureSet.random(seed,lecture_name) for _ in range(lecture_count)]
		exam_count = seed.randint(0, 4)
		exam_set = [ExamSet.random(seed,lecture_name,field) for _ in range(exam_count)]
		return cls(
			id=seed.randint(1,100),
			course_code=course_code,
			course_numbering=f"[{course_code}]",
			name=lecture_name,
			field=field,
			lecture_set=lecture_set,
			exam_set=exam_set,
			exam_count=exam_count,
		)


@dataclass_json
@dataclass
class KUWiki:
	count: int
	next: Optional[str]
	previous: Optional[str]
	results: List[Result]

	@classmethod
	def random(cls, seed:random.Random, lecture_name: str)->'KUWiki':
		return cls(
			count=1,
			next=None,
			previous=None,
			results=[
				Result.random(seed,lecture_name)
			]
		)


with open('shizen_chirigaku.json', 'r', encoding='utf-8') as f:
	shizen_chirigaku = KUWiki.from_json(f.read())
	# print(shizen_chirigaku)

def get_random_kuwiki(lecture_name: str)->KUWiki:
	if lecture_name == '自然地理学':
		return shizen_chirigaku

	length = len(lecture_name) % 10
	rand = random.Random(length)
	return KUWiki.random(rand, lecture_name)

if __name__=='__main__':
	print('===')
	print(get_random_kuwiki('自然地理学'))
	print('===')
	print(get_random_kuwiki('数理統計'))
	print('===')
	print(get_random_kuwiki('物理学実験'))
	print('===')
	print(get_random_kuwiki('数理統計'))
