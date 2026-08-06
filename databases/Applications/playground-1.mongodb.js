// FIT3171 Applied 1
// applied1_student.mongodb.js

// student id: 12345678
// student name: Angus
// last modified date: 3/03/2025

use ("aash0030");

db.student.drop();

db.student.insertMany[]

db.student.find();

db.student.find({"address":{$regex: /Moorabbin$/}});

db.student.find({"address":{$regex: /Moorabbin$/}},{"_id":0,"firstName":1,"lastName":1});