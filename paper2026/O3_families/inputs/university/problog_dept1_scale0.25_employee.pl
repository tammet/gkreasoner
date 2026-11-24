0.27::university(univ0).
0.96::department(dept0).
0.17::subOrganizationOf(dept0,univ0).
0.72::fullProfessor(full0_d0).
0.13::worksFor(full0_d0,dept0).
0.29::doctoralDegreeFrom(full0_d0,univ2).
1.00::emailAddress(full0_d0,mail_full0_d0).
0.25::researchInterest(full0_d0,res18).
0.66::fullProfessor(full1_d0).
0.49::worksFor(full1_d0,dept0).
0.48::doctoralDegreeFrom(full1_d0,univ1).
0.52::emailAddress(full1_d0,mail_full1_d0).
0.23::researchInterest(full1_d0,res8).
0.84::associateProfessor(asso0_d0).
0.14::worksFor(asso0_d0,dept0).
0.27::doctoralDegreeFrom(asso0_d0,univ1).
0.07::emailAddress(asso0_d0,mail_asso0_d0).
0.30::researchInterest(asso0_d0,res15).
0.44::associateProfessor(asso1_d0).
0.91::worksFor(asso1_d0,dept0).
0.41::doctoralDegreeFrom(asso1_d0,univ7).
0.16::emailAddress(asso1_d0,mail_asso1_d0).
0.30::researchInterest(asso1_d0,res15).
0.99::assistantProfessor(assi0_d0).
0.11::worksFor(assi0_d0,dept0).
0.64::doctoralDegreeFrom(assi0_d0,univ6).
0.41::emailAddress(assi0_d0,mail_assi0_d0).
0.68::researchInterest(assi0_d0,res6).
0.37::assistantProfessor(assi1_d0).
0.71::worksFor(assi1_d0,dept0).
0.52::doctoralDegreeFrom(assi1_d0,univ1).
0.67::emailAddress(assi1_d0,mail_assi1_d0).
0.91::researchInterest(assi1_d0,res15).
0.60::lecturer(lect0_d0).
0.19::worksFor(lect0_d0,dept0).
0.11::doctoralDegreeFrom(lect0_d0,univ0).
0.95::emailAddress(lect0_d0,mail_lect0_d0).
0.51::researchInterest(lect0_d0,res12).
0.23::headOf(full0_d0,dept0).
0.95::course(course0_d0).
0.60::teacherOf(asso1_d0,course0_d0).
0.74::course(course1_d0).
0.89::teacherOf(assi0_d0,course1_d0).
0.32::course(course2_d0).
0.39::teacherOf(lect0_d0,course2_d0).
0.88::course(course3_d0).
0.18::teacherOf(lect0_d0,course3_d0).
0.78::course(course4_d0).
0.14::teacherOf(full0_d0,course4_d0).
0.71::graduateCourse(gradCourse0_d0).
0.72::teacherOf(assi1_d0,gradCourse0_d0).
0.95::graduateCourse(gradCourse1_d0).
0.85::teacherOf(asso1_d0,gradCourse1_d0).
0.53::undergraduateStudent(ugrad0_d0).
0.24::memberOf(ugrad0_d0,dept0).
0.19::takesCourse(ugrad0_d0,course2_d0).
0.55::takesCourse(ugrad0_d0,course3_d0).
0.53::undergraduateStudent(ugrad1_d0).
0.12::memberOf(ugrad1_d0,dept0).
0.91::takesCourse(ugrad1_d0,course0_d0).
0.53::takesCourse(ugrad1_d0,course1_d0).
0.72::advisor(ugrad1_d0,full0_d0).
0.26::undergraduateStudent(ugrad2_d0).
0.28::memberOf(ugrad2_d0,dept0).
0.06::takesCourse(ugrad2_d0,course0_d0).
0.38::takesCourse(ugrad2_d0,course1_d0).
0.30::undergraduateStudent(ugrad3_d0).
0.45::memberOf(ugrad3_d0,dept0).
0.41::takesCourse(ugrad3_d0,course3_d0).
0.84::takesCourse(ugrad3_d0,course2_d0).
0.90::advisor(ugrad3_d0,full1_d0).
0.22::undergraduateStudent(ugrad4_d0).
0.43::memberOf(ugrad4_d0,dept0).
0.21::takesCourse(ugrad4_d0,course3_d0).
0.68::takesCourse(ugrad4_d0,course1_d0).
0.98::undergraduateStudent(ugrad5_d0).
0.24::memberOf(ugrad5_d0,dept0).
0.78::takesCourse(ugrad5_d0,course2_d0).
0.34::takesCourse(ugrad5_d0,course0_d0).
0.06::undergraduateStudent(ugrad6_d0).
0.78::memberOf(ugrad6_d0,dept0).
0.37::takesCourse(ugrad6_d0,course3_d0).
0.21::takesCourse(ugrad6_d0,course1_d0).
0.46::undergraduateStudent(ugrad7_d0).
0.27::memberOf(ugrad7_d0,dept0).
0.44::takesCourse(ugrad7_d0,course3_d0).
0.47::takesCourse(ugrad7_d0,course2_d0).
0.45::undergraduateStudent(ugrad8_d0).
0.61::memberOf(ugrad8_d0,dept0).
0.32::takesCourse(ugrad8_d0,course0_d0).
0.14::takesCourse(ugrad8_d0,course3_d0).
0.13::undergraduateStudent(ugrad9_d0).
0.15::memberOf(ugrad9_d0,dept0).
0.54::takesCourse(ugrad9_d0,course2_d0).
0.39::takesCourse(ugrad9_d0,course0_d0).
0.82::undergraduateStudent(ugrad10_d0).
0.53::memberOf(ugrad10_d0,dept0).
0.72::takesCourse(ugrad10_d0,course3_d0).
0.98::takesCourse(ugrad10_d0,course2_d0).
0.11::undergraduateStudent(ugrad11_d0).
0.07::memberOf(ugrad11_d0,dept0).
0.18::takesCourse(ugrad11_d0,course1_d0).
0.42::takesCourse(ugrad11_d0,course3_d0).
0.59::undergraduateStudent(ugrad12_d0).
0.76::memberOf(ugrad12_d0,dept0).
0.38::takesCourse(ugrad12_d0,course3_d0).
0.97::takesCourse(ugrad12_d0,course2_d0).
0.05::undergraduateStudent(ugrad13_d0).
0.84::memberOf(ugrad13_d0,dept0).
0.25::takesCourse(ugrad13_d0,course0_d0).
0.88::takesCourse(ugrad13_d0,course1_d0).
0.08::undergraduateStudent(ugrad14_d0).
0.97::memberOf(ugrad14_d0,dept0).
0.77::takesCourse(ugrad14_d0,course3_d0).
0.99::takesCourse(ugrad14_d0,course1_d0).
0.60::undergraduateStudent(ugrad15_d0).
0.22::memberOf(ugrad15_d0,dept0).
0.97::takesCourse(ugrad15_d0,course2_d0).
0.47::takesCourse(ugrad15_d0,course3_d0).
0.13::undergraduateStudent(ugrad16_d0).
0.63::memberOf(ugrad16_d0,dept0).
0.52::takesCourse(ugrad16_d0,course2_d0).
0.50::takesCourse(ugrad16_d0,course0_d0).
0.20::undergraduateStudent(ugrad17_d0).
0.17::memberOf(ugrad17_d0,dept0).
0.60::takesCourse(ugrad17_d0,course0_d0).
0.48::takesCourse(ugrad17_d0,course3_d0).
0.17::undergraduateStudent(ugrad18_d0).
0.47::memberOf(ugrad18_d0,dept0).
0.74::takesCourse(ugrad18_d0,course3_d0).
0.73::takesCourse(ugrad18_d0,course1_d0).
0.50::undergraduateStudent(ugrad19_d0).
0.42::memberOf(ugrad19_d0,dept0).
0.39::takesCourse(ugrad19_d0,course0_d0).
0.26::takesCourse(ugrad19_d0,course1_d0).
0.24::advisor(ugrad19_d0,assi1_d0).
0.47::undergraduateStudent(ugrad20_d0).
0.15::memberOf(ugrad20_d0,dept0).
0.74::takesCourse(ugrad20_d0,course3_d0).
0.72::takesCourse(ugrad20_d0,course2_d0).
0.63::advisor(ugrad20_d0,assi0_d0).
0.07::undergraduateStudent(ugrad21_d0).
0.40::memberOf(ugrad21_d0,dept0).
0.46::takesCourse(ugrad21_d0,course1_d0).
0.14::takesCourse(ugrad21_d0,course0_d0).
0.97::undergraduateStudent(ugrad22_d0).
0.77::memberOf(ugrad22_d0,dept0).
0.53::takesCourse(ugrad22_d0,course1_d0).
0.72::takesCourse(ugrad22_d0,course3_d0).
0.24::undergraduateStudent(ugrad23_d0).
0.27::memberOf(ugrad23_d0,dept0).
0.55::takesCourse(ugrad23_d0,course2_d0).
0.76::takesCourse(ugrad23_d0,course1_d0).
0.66::undergraduateStudent(ugrad24_d0).
0.06::memberOf(ugrad24_d0,dept0).
0.63::takesCourse(ugrad24_d0,course0_d0).
0.91::takesCourse(ugrad24_d0,course1_d0).
0.76::undergraduateStudent(ugrad25_d0).
0.93::memberOf(ugrad25_d0,dept0).
0.98::takesCourse(ugrad25_d0,course1_d0).
0.26::takesCourse(ugrad25_d0,course2_d0).
0.33::undergraduateStudent(ugrad26_d0).
0.57::memberOf(ugrad26_d0,dept0).
0.98::takesCourse(ugrad26_d0,course1_d0).
0.40::takesCourse(ugrad26_d0,course3_d0).
0.94::undergraduateStudent(ugrad27_d0).
0.86::memberOf(ugrad27_d0,dept0).
0.54::takesCourse(ugrad27_d0,course3_d0).
0.64::takesCourse(ugrad27_d0,course1_d0).
0.96::undergraduateStudent(ugrad28_d0).
0.79::memberOf(ugrad28_d0,dept0).
0.33::takesCourse(ugrad28_d0,course1_d0).
0.85::takesCourse(ugrad28_d0,course2_d0).
0.24::undergraduateStudent(ugrad29_d0).
0.40::memberOf(ugrad29_d0,dept0).
0.96::takesCourse(ugrad29_d0,course2_d0).
0.85::takesCourse(ugrad29_d0,course1_d0).
0.35::undergraduateStudent(ugrad30_d0).
0.33::memberOf(ugrad30_d0,dept0).
0.63::takesCourse(ugrad30_d0,course2_d0).
0.85::takesCourse(ugrad30_d0,course1_d0).
0.70::undergraduateStudent(ugrad31_d0).
0.94::memberOf(ugrad31_d0,dept0).
0.74::takesCourse(ugrad31_d0,course1_d0).
0.83::takesCourse(ugrad31_d0,course2_d0).
0.62::advisor(ugrad31_d0,assi0_d0).
0.39::undergraduateStudent(ugrad32_d0).
0.46::memberOf(ugrad32_d0,dept0).
0.52::takesCourse(ugrad32_d0,course1_d0).
0.55::takesCourse(ugrad32_d0,course0_d0).
0.85::undergraduateStudent(ugrad33_d0).
0.31::memberOf(ugrad33_d0,dept0).
0.12::takesCourse(ugrad33_d0,course2_d0).
0.75::takesCourse(ugrad33_d0,course0_d0).
0.31::undergraduateStudent(ugrad34_d0).
0.45::memberOf(ugrad34_d0,dept0).
0.16::takesCourse(ugrad34_d0,course0_d0).
0.84::takesCourse(ugrad34_d0,course3_d0).
0.31::undergraduateStudent(ugrad35_d0).
0.33::memberOf(ugrad35_d0,dept0).
0.81::takesCourse(ugrad35_d0,course3_d0).
0.53::takesCourse(ugrad35_d0,course0_d0).
0.31::undergraduateStudent(ugrad36_d0).
0.89::memberOf(ugrad36_d0,dept0).
0.44::takesCourse(ugrad36_d0,course2_d0).
0.39::takesCourse(ugrad36_d0,course0_d0).
0.97::graduateStudent(grad0_d0).
0.80::memberOf(grad0_d0,dept0).
0.76::undergraduateDegreeFrom(grad0_d0,univ9).
0.29::advisor(grad0_d0,full1_d0).
0.82::takesCourse(grad0_d0,gradCourse0_d0).
0.62::takesCourse(grad0_d0,gradCourse1_d0).
0.84::teachingAssistantOf(grad0_d0,course1_d0).
0.40::graduateStudent(grad1_d0).
0.79::memberOf(grad1_d0,dept0).
0.80::undergraduateDegreeFrom(grad1_d0,univ4).
0.42::advisor(grad1_d0,assi0_d0).
0.67::takesCourse(grad1_d0,course4_d0).
0.79::takesCourse(grad1_d0,gradCourse0_d0).
0.99::graduateStudent(grad2_d0).
0.92::memberOf(grad2_d0,dept0).
0.80::undergraduateDegreeFrom(grad2_d0,univ4).
0.18::advisor(grad2_d0,asso1_d0).
0.63::takesCourse(grad2_d0,gradCourse1_d0).
0.70::takesCourse(grad2_d0,gradCourse0_d0).
0.13::graduateStudent(grad3_d0).
0.49::memberOf(grad3_d0,dept0).
0.88::undergraduateDegreeFrom(grad3_d0,univ1).
0.91::advisor(grad3_d0,full0_d0).
0.93::takesCourse(grad3_d0,gradCourse0_d0).
0.14::takesCourse(grad3_d0,gradCourse1_d0).
0.63::graduateStudent(grad4_d0).
0.87::memberOf(grad4_d0,dept0).
0.67::undergraduateDegreeFrom(grad4_d0,univ3).
0.35::advisor(grad4_d0,asso0_d0).
0.09::takesCourse(grad4_d0,course4_d0).
0.92::takesCourse(grad4_d0,gradCourse0_d0).
0.87::graduateStudent(grad5_d0).
0.67::memberOf(grad5_d0,dept0).
0.40::undergraduateDegreeFrom(grad5_d0,univ8).
0.84::advisor(grad5_d0,full1_d0).
0.82::takesCourse(grad5_d0,gradCourse1_d0).
0.74::takesCourse(grad5_d0,gradCourse0_d0).
0.62::graduateStudent(grad6_d0).
0.35::memberOf(grad6_d0,dept0).
0.33::undergraduateDegreeFrom(grad6_d0,univ0).
0.39::advisor(grad6_d0,full1_d0).
0.36::takesCourse(grad6_d0,course4_d0).
0.54::takesCourse(grad6_d0,gradCourse0_d0).
0.16::teachingAssistantOf(grad6_d0,course1_d0).
0.74::graduateStudent(grad7_d0).
0.38::memberOf(grad7_d0,dept0).
0.20::undergraduateDegreeFrom(grad7_d0,univ7).
0.29::advisor(grad7_d0,assi1_d0).
0.42::takesCourse(grad7_d0,gradCourse1_d0).
0.46::takesCourse(grad7_d0,gradCourse0_d0).
0.79::graduateStudent(grad8_d0).
0.14::memberOf(grad8_d0,dept0).
0.26::undergraduateDegreeFrom(grad8_d0,univ3).
0.33::advisor(grad8_d0,assi1_d0).
0.22::takesCourse(grad8_d0,gradCourse1_d0).
0.76::takesCourse(grad8_d0,gradCourse0_d0).
0.15::teachingAssistantOf(grad8_d0,course0_d0).
0.10::graduateStudent(grad9_d0).
0.58::memberOf(grad9_d0,dept0).
0.75::undergraduateDegreeFrom(grad9_d0,univ6).
0.83::advisor(grad9_d0,assi1_d0).
0.58::takesCourse(grad9_d0,gradCourse1_d0).
0.36::takesCourse(grad9_d0,gradCourse0_d0).
0.89::publication(pub0_d0).
0.75::publicationAuthor(pub0_d0,asso1_d0).
0.50::publicationAuthor(pub0_d0,ugrad19_d0).
0.58::publication(pub1_d0).
0.94::publicationAuthor(pub1_d0,full1_d0).
1.00::publication(pub2_d0).
0.93::publicationAuthor(pub2_d0,full0_d0).
0.18::publicationAuthor(pub2_d0,ugrad4_d0).
0.36::publication(pub3_d0).
0.44::publicationAuthor(pub3_d0,asso0_d0).
0.21::publication(pub4_d0).
0.77::publicationAuthor(pub4_d0,asso0_d0).
0.11::publication(pub5_d0).
0.89::publicationAuthor(pub5_d0,asso1_d0).
0.61::publication(pub6_d0).
0.63::publicationAuthor(pub6_d0,full1_d0).
0.44::publicationAuthor(pub6_d0,ugrad2_d0).
0.94::publication(pub7_d0).
0.60::publicationAuthor(pub7_d0,assi0_d0).
0.90::publication(pub8_d0).
0.93::publicationAuthor(pub8_d0,assi0_d0).
0.71::publicationAuthor(pub8_d0,grad8_d0).
0.98::publication(pub9_d0).
0.52::publicationAuthor(pub9_d0,assi0_d0).
0.40::publication(pub10_d0).
0.85::publicationAuthor(pub10_d0,asso1_d0).
0.55::publicationAuthor(pub10_d0,ugrad6_d0).
0.34::publication(pub11_d0).
0.70::publicationAuthor(pub11_d0,full1_d0).
0.50::publication(pub12_d0).
0.17::publicationAuthor(pub12_d0,asso1_d0).
0.85::publication(pub13_d0).
0.52::publicationAuthor(pub13_d0,asso1_d0).
0.97::publicationAuthor(pub13_d0,grad5_d0).
0.56::publication(pub14_d0).
0.94::publicationAuthor(pub14_d0,asso1_d0).
0.32::publicationAuthor(pub14_d0,ugrad31_d0).
course(X) :- graduateCourse(X).
course(Y) :- teacherOf(X,Y).
course(Y) :- teachingAssistantOf(X,Y).
degreeFrom(X,Y) :- doctoralDegreeFrom(X,Y).
degreeFrom(X,Y) :- undergraduateDegreeFrom(X,Y).
faculty(X) :- lecturer(X).
faculty(X) :- teacherOf(X,Y).
hasAlumnus(Y,X) :- degreeFrom(X,Y).
member(Y,X) :- memberOf(X,Y).
memberOf(X,Y) :- worksFor(X,Y).
memberOf(Y,X) :- member(X,Y).
organization(X) :- department(X).
organization(X) :- member(X,Y).
organization(X) :- subOrganizationOf(X,Y).
organization(X) :- university(X).
organization(Y) :- subOrganizationOf(X,Y).
person(X) :- advisor(X,Y).
person(X) :- degreeFrom(X,Y).
person(X) :- doctoralDegreeFrom(X,Y).
person(X) :- emailAddress(X,Y).
person(X) :- graduateStudent(X).
person(X) :- undergraduateDegreeFrom(X,Y).
person(Y) :- hasAlumnus(X,Y).
person(Y) :- member(X,Y).
person(Y) :- publicationAuthor(X,Y).
professor(X) :- assistantProfessor(X).
professor(X) :- associateProfessor(X).
professor(X) :- fullProfessor(X).
professor(Y) :- advisor(X,Y).
publication(X) :- publicationAuthor(X,Y).
student(X) :- undergraduateStudent(X).
subOrganizationOf(X,Z) :- subOrganizationOf(X,Y), subOrganizationOf(Y,Z).
teachingAssistant(X) :- teachingAssistantOf(X,Y).
university(X) :- hasAlumnus(X,Y).
university(Y) :- degreeFrom(X,Y).
university(Y) :- doctoralDegreeFrom(X,Y).
university(Y) :- undergraduateDegreeFrom(X,Y).
work(X) :- course(X).
worksFor(X,Y) :- headOf(X,Y).
degreeFrom(Y,X) :- hasAlumnus(X,Y).
employee(X) :- faculty(X).
faculty(X) :- professor(X).
query(employee(full1_d0)).
