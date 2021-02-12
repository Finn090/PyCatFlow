import drawSvg as draw
import pycatflow as pcf

def genSVG(nodes,spacing,width=None,heigth=None,nodes_color="start_end",show_labels=True,label_text="tag",label_shortening="clip"):
    headers=nodes[0]
    
    sequence=nodes[2]
    n_x_spacing=spacing
    n_y_spacing=spacing+(spacing/5)
    #h_x_shift=[n_x_spacing]
    points=[]
    for n in nodes[1]:
        
        if n.index>0 and n.x==nodes[1][n.index-1].x:
            n_y_spacing+=spacing/5
        else:
            n_y_spacing=spacing*2
        if n.index>0 and n.x!=nodes[1][n.index-1].x:
            n_x_spacing+=spacing
            #h_x_shift.append(n.x+n_x_spacing)
        points.append(pcf.Node(n.index,n.x+ n_x_spacing,n.y+n_y_spacing,n.size,n.width,n.label,n.subtag))
    
    
    if width is None and heigth is None:
        
        width=spacing*4+max([x.x for x in points])
        heigth=spacing*4+max([x.y for x in points])
        
    elif heigth is None:
        heigth=spacing*4+max([x.y for x in points])
        points=[pcf.Node(n.index,(n.x*(width-spacing*2)/max([x.x for x in points])),n.y,n.size,n.width,n.label,n.subtag) for n in points]
    elif width is None:
        width=spacing*4+max([x.x for x in points])
        points=[pcf.Node(n.index,n.x,(n.y*(heigth-spacing)/max([x.y for x in points])),n.size,n.width,n.label,n.subtag) for n in points]
    else:  
        points=[pcf.Node(n.index,(n.x*(width-spacing)/max([x.x for x in points])),(n.y*(heigth-spacing)/max([x.y for x in points])),n.size,n.width,n.label,n.subtag) for n in points]      

          

    
        
    
    d = draw.Drawing(width, heigth,displayInline=True)
    r = draw.Rectangle(0,0,width,heigth, stroke_width=2, stroke='black',fill="white")
    d.append(r)

    #headers
    h_x_shift=[points[0].x]
    for x in points:
        if x.x!=points[x.index-1].x and x.index>0:
            h_x_shift.append(x.x)
    
    for h,x in zip (headers,h_x_shift):
        d.append(draw.Text(h,x=x,y=heigth-spacing,fontSize=5))
    
    #lines
    for n in sequence.items():
        p = draw.Path(stroke_width=points[n[1][0]].size, stroke='gray',stroke_linejoin="round",stroke_opacity="0.5",fill="transparent")
        if len(n[1])>1:            
            p.M(points[n[1][0]].x,heigth-points[n[1][0]].y+points[n[1][0]].size/2)
            #d.append(draw.Circle(nodes[1][n[1][0]],heigth-nodes[2][n[1][0]]+nodes[3][n[1][0]]/2,2,fill="red"))
            p.L(points[n[1][0]].x+points[n[1][0]].width,heigth-points[n[1][0]].y+points[n[1][0]].size/2)
            #d.append(draw.Circle(nodes[1][n[1][0]]+size,heigth-nodes[2][n[1][0]]+nodes[3][n[1][0]]/2,2,fill="red"))
            for k in n[1][1:]:
                if points[k].y==points[n[1][n[1].index(k)-1]].y:
                    p.L(points[k].x,heigth-points[k].y+points[n[1][0]].size/2)
                    #d.append(draw.Circle(nodes[1][k],heigth-nodes[2][k]+nodes[3][n[1][0]]/2,2,fill="green"))                
                    p.L(points[k].x+points[k].width,heigth-points[k].y+points[n[1][0]].size/2)
                    #d.append(draw.Circle(nodes[1][k]+size,heigth-nodes[2][k]+nodes[3][n[1][0]]/2,2,fill="green"))
                else:
                    yMedium=(heigth-points[n[1][n[1].index(k)-1]].y+points[n[1][0]].size/2)+(((heigth-(points[k].y+points[n[1][0]].size/2))-(heigth-points[n[1][n[1].index(k)-1]].y+points[n[1][0]].size/2))/2)
                    p.Q(points[k].x-(spacing/2),heigth-points[n[1][n[1].index(k)-1]].y+points[n[1][0]].size/2,points[k].x-(spacing/2),yMedium)
                    #d.append(draw.Circle(nodes[1][k]-(spacing/2),heigth-nodes[2][n[1][n[1].index(k)-1]]+nodes[3][n[1][0]]/2,2,fill="blue"))
                    #d.append(draw.Circle(nodes[1][k]-(spacing/2),yMedium,2,fill="red"))
                    p.Q(points[k].x-(spacing/2),heigth-points[k].y+points[n[1][0]].size/2,points[k].x,heigth-points[k].y+points[n[1][0]].size/2)
                    #p.T(nodes[1][k],heigth-nodes[2][k]+nodes[3][n[1][0]]/2)
                    #d.append(draw.Circle(nodes[1][k]-(spacing/3),heigth-nodes[2][k]+nodes[3][n[1][0]]/2,2,fill="black"))
                    #d.append(draw.Circle(nodes[1][k],heigth-nodes[2][k]+nodes[3][n[1][0]]/2,2,fill="green"))
                    p.L(points[k].x+points[k].width,heigth-points[k].y+points[n[1][0]].size/2)
                    #d.append(draw.Circle(nodes[1][k]+size,heigth-nodes[2][k]+nodes[3][n[1][0]]/2,2,fill="green"))
                    
            d.append(p)            

    #nodes
    #n_x_shift=spacing
    #n_y_shift=spacing
    for node in points:
        if nodes_color == "start_end":
            if node.label not in [n.label for n in points][:node.index]:
                color="green"
            elif node.label not in [n.label for n in points][node.index+1:]:
                color="red"
            else:
                color="gray"
        elif nodes_color == "subtag":
            for e in set([n.subtag for n in points]):
                if e==node.subtag:
                    color="rgb("+str([n.subtag for n in points].index(node.subtag)*10)+",100,100)"
        #if node.x!=points[node.index-1].x:
            #n_x_shift+=spacing
        r = draw.Rectangle(node.x,heigth-node.y,node.width,node.size, fill=color,stroke="black")
        d.append(r)


        if show_labels==True:
            
            if label_text=="tag_count":
                txt=node.label+' ('+str(node.size)+')'
            elif label_text=="tag":
                txt=node.label
            elif label_text=="tag_subtag":
                txt=node.label+' ('+str(node.subtag)+')'                           
                
            if label_shortening=="resize":
                label= draw.Text(txt,x=node.x+node.width+(spacing/8),y=heigth-node.y+(node.size/2),fontSize=5,textLength=spacing-2*(spacing/8))
            elif label_shortening=="clip":
                clip = draw.ClipPath()
                clip.append(draw.Rectangle(node.x+node.width,heigth-node.y,spacing-(spacing/8),node.size))
                label= draw.Text(txt,x=node.x+node.width+(spacing/8),y=heigth-node.y+(node.size/2),fontSize=5,clip_path=clip)
            d.append(label)

    return d
