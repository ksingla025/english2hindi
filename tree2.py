import os
import sys
import re

debug=False
if len(sys.argv)>1:
	debug=True
	print
	print "LOADING-WAIT---------------------------------------------------------------------------"
	print
pi=os.getpid()
sentence="I am Karan"
os.popen("echo '"+sentence+"' > ./stanford-parser-full-2014-01-04/stanfordtemp.txt."+str(pi))

parser_out = os.popen("./stanford-parser-full-2014-01-04/lexparser.sh ./stanford-parser-full-2014-01-04/stanfordtemp.txt."+str(pi)).readlines()
if debug==True:
	print
	print "---------------------------------------------------------------------------------------"
	print "{DebugMode}",
	print "Enter sentence- "
	print
errors=[]
pre=""
coun = 0
counter = 0
for i in sys.stdin:
	
        coun += 1
	def print_leaves(s):
		if len(s.children)==0:
			x=s.data
			c=0
			for i in x:
				if i==" ":
					break
				c+=1
			print s.data[c+1::],		
		for i in s.children:
			print_leaves(i)

	xx=str(i)
	lx=map(str,xx.split())
	#print lx
	px=[]	
	qx=[]
	for i in lx:
		px.append(map(str,i.split("_"))[0])
		qx.append(map(str,i.split("_"))[1])
	#print px
	#print qx
		
	sentence=""
	cx=len(px)
	for i in xrange(cx):
		sentence+=px[i]
		if i!=cx:
			sentence+=" "
	#print sentence
	#sentence=str(i)
	new=""
	for i in sentence:
		if i=="'":
			new+="'"
		new+=i
	sentence=new
	pre=parser_out
	if len(sentence)>250:
		sys.stdout.write("ERROR -sentence too long !!!\n");
		errors.append(str(coun)+" ERROR -sentence too long\n")
		continue
	os.popen("echo '"+sentence+"' > ./stanford-parser-full-2014-01-04/stanfordtemp.txt."+str(pi))
	parser_out = os.popen("./stanford-parser-full-2014-01-04/lexparser.sh ./stanford-parser-full-2014-01-04/stanfordtemp.txt."+str(pi)).readlines()
	if pre==parser_out:
		sys.stdout.write("ERROR -parser error !!!\n")
		errors.append(str(coun)+" ERROR -parser error !!!\n")
		continue
	if debug==True:
		print
		print "parser_out-------------------------------"
		print
		print parser_out
		print
		print "tree-------------------------------------"
		print
		for tree in parser_out:
			print tree
		print
		print "compact_format---------------------------"
		print
#	print "----------"
#	print parser_out
#	print "----------"
	
	count=0
	flag1=0
	flag2=0
	compact=""
	for i in parser_out:
		flag3=0
		for j in i:
			if j=='(':
				count+=1
			if j==')':
				count-=1
			if j!=" ":
				flag3=1
			if j!='\n' and (j!=" " or flag3==1):
				compact+=j
			if count==0 and flag1==0:
				flag1=1
			elif count==0 and flag1==1:
				flag2=1
				break
		if flag2==1:
			break
	if debug==True:
		print compact
		print
		print "readable_format----------------------"
		print
	read=[]
	flag1=0
	flag2=0
	i=0
	j=0
	l=len(compact)
	for k in xrange(l):
		if compact[k]=='(' or k==l-1:
			j=k
			read.append(compact[i:j])
			i=k
	read=read[1::]
	#print "------------d"
#	print read
#	for i in read:
#		print i
	vx=len(read)
	coux=0
	for ix in xrange(vx):
		zx=len(read[ix])
		for jx in xrange(zx):
			if read[ix][jx]==')':
#				print "he"
				if read[ix][jx-1]!=')':
					#print "re"
					tempx=read[ix][0:jx]+"_"+qx[coux]+read[ix][jx::]
					read[ix]=tempx
					coux+=1
					break
			
#	for i in read:
#		print i
	
#	print "------------e"
	if debug==True:
		for i in read:
			print i
		print
		print "making_tree-------------------------"
		print
	class Node:
		def __init__(self,data):	
			c=0
			x=data
			d=0
			for i in x:
				if i==')':
					break
				d+=1
			data=str(x[c+1:d])
			self.data=data
			self.children=[]
	def make_tree(s):
		stack=[]
		cur=None
		root=None
	
		l=len(s)
		for i in xrange(l):
			cur=Node(s[i])
			if len(stack)>0:
				stack[-1].children.append(cur)
			stack.append(cur)
			if root is None:
				root=cur
			for j in s[i]:
				if j==')':
					l=len(stack)
					stack=stack[0:l-1]
		return root
	
	root=make_tree(read)
	if debug==True:
		print
		print "applying_rules-----------------------"
		print



	def get_type(s):	
		x=s.data
		c=0
		for i in x:
			if i==" ":
				break
			c+=1
		x=(s.data)[0:c]
		return x
	
		

	if debug==True:
		print
		print "------------------------------------"
		print "Original-"
		print_leaves(root)
		print
		print "Rule_1"
	def rule1(s):
		x=get_type(s)
		if x=="VP" or x=="PP" or x=="WHPP":
			s.children=s.children[::-1]
		for i in s.children:
			rule1(i)
	rule1(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_2"
			
	def rule2(s):
		x=get_type(s)
		if x=="ADVP":
			s.children=s.children[::-1]
		for i in s.children:
			rule2(i)
	rule2(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_3"
	def rule3(s):
		x=get_type(s)
		if x=="ADVP":
			if len(s.children)>0:
				x=get_type(s.children[0])
				if x=="RB":
					s.children=s.children[::-1]
		for i in s.children:
			rule3(i)
	rule3(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_4"
	def rule4(s):
		x=get_type(s)
		if x=="ADJP":
			if len(s.children)>0:
				x=get_type(s.children[-1])
				if x=="PP" or "S":
					s.children=s.children[::-1]
		for i in s.children:
			rule4(i)
	rule4(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_5"
	def rule5(s):
		x=get_type(s)
		if x=="ADJP":
			c=0
			for j in s.children:
				y=get_type(j)
				if y=="RB":
					c=1
					break
			if c==1:
				s.children=s.children[::-1]
		for i in s.children:
			rule5(i)
	rule5(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_6"
	def rule6(s):
		x=get_type(s)
		if x=="SBARQ":
			if len(s.children)>=2:
				y=get_type(s.children[0])
				z=get_type(s.children[1])
				if y=="WHNP" and ( z=="S" or z=="SQ"):
					r=s.children[0]
					l=len(s.children)
					s.children=s.children[1:l]
					t=s.children[0]
					temp=[]
					for i in t.children:
						if get_type(i)=="VP":
							temp.append(r)
						temp.append(i)
					t.children=temp
					s.children[0]=t
		for i in s.children:
			rule6(i)		
	rule6(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_7"



	def rule7(s):
		x=get_type(s)
		if x=="SQ":
			if len(s.children)>=2:
				y=get_type(s.children[0])
				z=get_type(s.children[1])
				if y=="MD" or y=="VB" or y=="VBN" or y=="VBZ" or y=="VBD" or y=="VBP" or y=="VBZ":
					if z=="NP":
						x="VPc"
						temp1=Node(x)
						temp2=s.children[0]
						s.children[0]=s.children[1]
						s.children[1]=temp1
						l=len(s.children)
						s.children[1].children.append(temp2)
						for i in xrange(2,l):
							s.children[1].children.append(s.children[i])
						s.children=s.children[0:2]
		for i in s.children:
		     	rule7(i)
						



	rule7(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_8"
	def rule8(s):
		x=get_type(s)
		if x=="NP":
			if len(s.children)>1:
				if get_type(s.children[-1])=="S":
					l=len(s.children)
					t=s.children[-1]
					temp=s.children[0:l-1]
					s.children=[t]+temp
		for i in s.children:
			rule8(i)
	rule8(root)
	if debug==True:
		print_leaves(root)
		print
		print "Rule_10"
	def rule10(s):
		x=get_type(s)
		if x=="NP":
			if len(s.children)>1:
				if get_type(s.children[0])=="NP" and ( get_type(s.children[1])=="PP" or get_type(s.children[1])=="SBAR"):
					s.children=s.children[::-1]
		for i in s.children:
			rule10(i)
	rule10(root)
	if debug ==True:
		print_leaves(root)
		print
		print "Rule_11"
	v=["VBN","VBZ","VBD","VBP","VP"]
	def rule11(s):
		x=get_type(s)
		if x=="NP":
			if len(s.children)>1:
				if get_type(s.children[0])=="PDT" and (get_type(s.children[-1])=="N" or get_type(s.children[-1])=="NNS"):
					l=len(s.children)
					t1=s.children[0]
					t2=s.children[-1]
					t3=s.children[1:l-1]
					s.children=t3+[t1]+[t2]
		for i in s.children:
			rule11(i)
	rule11(root)
	if debug==True:
	 	print_leaves(root)
		print
		print "Rule_12"
	def rule12(s):
		x=get_type(s)
		if x=="VP":
			if len(s.children)>=2:
					if get_type(s.children[-2])=="ADVP":
						if get_type(s.children[-1])=="VP":
							if len(s.children[-1].children)>=1:
								if get_type(s.children[-1].children[0]) in v:
										print "dfFF"
										o=[]
										o.append(s.children[-2])
										for i in s.children[-1].children:
											o.append(i)
										s.children[-1].children=o
										s.children[-2]=s.children[-1]
										del s.children[-1]
		for i in s.children:
			rule12(i)		
	rule12(root)
	if debug==True:
	 	print_leaves(root)
		print
		print "Rule_14"
	
	def rule14(s):	
		x=get_type(s)
		if x=="VP":
			if len(s.children)>=2:
				if get_type(s.children[0])=="ADVP" and get_type(s.children[1]) in v:
					temp=s.children[1]
					s.children[1]=s.children[0]
					s.children[0]=temp
		for i in s.children:
			rule14(i)

	rule14(root)
	if debug==True:
	 	print_leaves(root)
		print
		print "Rule_15"
	def rule15(s):
		x=get_type(s)
		if x=="ADVP":
			if len(s.children)==2:
				if get_type(s.children[0])=="RB" and get_type(s.children[1])=="NP":
					temp=s.children[1]
					s.children[1]=s.children[0]
					s.children[0]=temp
		for i in s.children:
			rule15(i)


	rule15(root)
	if debug==True:
	 	print_leaves(root)
		print
		print "Rule_13"
	


	pre1=["a","abaft","aboard","about","above","absent","across","afore","after","against","along","alongside","amid","amidst","among","amongst","an","a","anenst","apropos","apropos of","apud","around","as","aside","astride","at","athwart","atop","barring","before","behind","below","beneath","beside","besides","between","beyond","but","by","circa","c.","ca.","concerning","despite","down","during","except","excluding","failing","following","for","forenenst","from","given","in","including","inside","into","like","mid","midst","minus","modulo","near","nigh","next","notwithstanding","o'","of","off","on","onto","opposite","out","outside","over","pace","past","per","plus","pro","qua","regarding","round","sans","save","since","than","through","thru","throughout","thruout","till","times","to","toward","towards","under","underneath","unlike","until","unto","up","upon","versus","via","vice","with","within","without","worth"]
	pre2=["according to","ahead of","apart from","as for","as of","as per","as regards","aside from","back to","because of","close to","due to","except for","far from","in to","inside of","instead of","left of","near to","next to","on to","out from","out of","outside of","owing to","prior to","pursuant to","rather than","regardless of","right of","subsequent to","such as","thanks to","that of","up to"]
	pre3=["as far as","as long as","as opposed to","as well as","as soon as"]
	pre4=["at the behest of","by means of","by virtue of","for the sake of","in accordance with","in addition to","in case of","in front of","in lieu of","in order to","in place of","in point of","in spite of","on account of","on behalf of","on top of","with regard to","with respect to","with a view to"]



	def get_data(s):
		x=s.data
		c=0
		for i in x:
			if i==" ":
				break
			c+=1
		return s.data[c+1::]

	def rule13(s):
		x=get_type(s)
		if x=="SBAR":
			if len(s.children)==2:
				if get_type(s.children[0])=="IN":
					if get_type(s.children[1])=="S":
						if len(s.children[0].children)==0:
							y=get_data(s.children[0])
							if y in pre1 or y in pre2 or y in pre3 or y in pre4:
								temp=s.children[0]
								s.children[0]=s.children[1]
								s.children[1]=temp
		for i in s.children:
		      rule13(i)
	rule13(root)
	if debug==True:
	 	print_leaves(root)
		print
		print "Rule_14_2"

	def rule14_2(s):
		x=get_type(s)
		if x=="XP":
			if len(s.children)>=2:
				if get_type(s.children[-1])=="PP":
					if get_type(s.children[-2])=="PP":
						y="FrozenP"
						n=Node(y)
						n.children.append(s.children[-2])
						n.children.append(s.children[-1])
						del s.children[-1]
						del s.children[-1]
						s.children.append(n)
		for i in s.children:
			rule14_2(i)

	rule14_2(root)
	if debug==True:
		print_leaves(root)
		print
		print
		print "printing_leaves-------------------------------------"
		print
	ans=""
	def final_print(s):
		if len(s.children)==0:
			global ans
			c=0
			for i in s.data:
				if i==" ":
					break
				c+=1
			ans+=str(s.data[c+1:])+" "
		for i in s.children:
			final_print(i)
	final_print(root)
	ans+="\n"
	sys.stdout.write(ans)
	if debug==True:
		print
		print "------------------------------------------------------"


	# FOR UNIT TESTING !!!  comment this later
	#-------------------------------------------
#	rule1(root)
#	rule2(root)
#	rule3(root)
#	rule4(root)
#	rule5(root)
#	rule6(root)
#	rule7(root)
#	rule8(root)
#	rule9(root) NOT DONE
#	rule10(root)
#	rule11(root)
#	rule12(root)
#	rule14(root)
#	rule15(root)
#	rule13(root)
#	rule14_2(root)
#	ans=""
#	final_print(root)
#	ans+="\n"
#	print ans
	
	#-------------------------------------------
rep="report.txt."+str(pi)
f=open(rep,'w')
x=""
for i in errors:
	x+=i
f.write(x)
f.close()

x="~/Avijit/stanford-parser-full-2014-01-04/stanfordtemp.txt."+str(pi)
#os.remove(x)
os.system("rm -rf "+x)
