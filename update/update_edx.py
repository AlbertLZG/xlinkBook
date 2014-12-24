#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *


class EdxSpider(Spider):
    
    def __init__(self):
        Spider.__init__(self)
    
        self.school = "edx"
        self.edx_subject = [\
        "Architecture",
        "Art & Culture",
        "Biology & Life Sciences",
        "Business & Management",
        "Chemistry",
        "Communication",
        "Computer Science",
        "Design",
        "Economics & Finance",
        "Education",
        "Electronics",
        "Energy & Earth Sciences",
        "Engineering",
        "Environmental Studies",
        "Ethics",
        "Food & Nutrition",
        "Health & Safety",
        "History",
        "Humanities",
        "Law",
        "Literature",
        "Math",
        "Medicine",
        "Music",
        "Philanthropy",
        "Philosophy & Ethics",
        "Physics",
        "Science",
        "Social Sciences",
        "Statistics & Data Analysis"]
    
    #edx
    
    def match_subject(self, subject, subjects):
        for sub in subjects:
            if sub != "" and sub.strip() == subject:
                return True
    
        return False
    
    
    def getEdxOnlineCourse(self, subject, json_obj):
        if self.need_update_subject(subject) == False:
            return
        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        count = 0
        print "processing json and write data to file..."
        for item in json_obj:
            if self.match_subject(subject, item["subjects"]):
                #for item in json_obj:
                title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
                title = self.delZh(title)
                count = count + 1
                self.write_db(f, item["code"].strip(), title, item["url"], item["availability"])
    
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n" 
        
    
    def do_work(self):
    
        print "downloading edx course info"
        r = requests.get("https://www.edx.org/search/api/all")
    
    
        print "loading data..."
        jobj = json.loads(r.text)
    
    
        for subject in self.edx_subject:
            if subject != "":
                self.getEdxOnlineCourse(subject, jobj)
    
start = EdxSpider()
start.do_work()
    
