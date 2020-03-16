from PIL import Image, ImageDraw, ImageFont
import random
class NewObject:
    def __init__(self, name="OBJECT"+str(random.randint(10000,99999)),text="OBJECT",cover='rectangle', row=1,column=1, bgcolor=(255,255,255),textcolor=(0,0,0),font=('cg.ttf', 20)):
        self.row=row
        self.column=column
        self.name=name
        self.text=text
        self.bgcolor=bgcolor
        self.textcolor=textcolor
        self.font=ImageFont.truetype(font[0],font[1])
        self.cover=cover
        self.connections=[]
        self.coordinates=()
        self.box_coordinates=()
class Chart:
    def __init__(self, width, height,background=(255,255,255)):
        self.width=width
        self.height=height
        self.canvas=Image.new('RGB',(self.width, self.height), background)
        self.draw=ImageDraw.Draw(self.canvas)
        self.tree=({},{})
        self.__object_rows={}
        self.__object_columns={}
        self.box_outline=(0,0,0)
        self.line_color=(0,0,0)
        self.line_thickness=3
    def connect_objects(self,obj1,obj2):
        if isinstance(obj1, NewObject) and isinstance(obj2, NewObject):
            if obj1.name in self.tree[0] and obj2.name in self.tree[0]:
                obj1.connections.append(obj2.name)
            else:
                raise Errors.ObjectNotInTable
        else:
            raise Errors.InvalidObject
    def __connect_objs(self, obj):
        if len(self.tree[1][obj].connections) != 0:
            for c in self.tree[1][obj].connections:
                if self.tree[1][obj].coordinates[0] < self.tree[1][c].coordinates[0]:
                    x1=self.tree[1][obj].box_coordinates[2]
                    y1=int((self.tree[1][obj].box_coordinates[1]+self.tree[1][obj].box_coordinates[3])/2)
                    x2=self.tree[1][c].box_coordinates[0]
                    y2=int((self.tree[1][c].box_coordinates[1]+self.tree[1][c].box_coordinates[3])/2)  
                elif self.tree[1][obj].coordinates[0] > self.tree[1][c].coordinates[0]: 
                    x1=self.tree[1][obj].box_coordinates[0]
                    y1=int((self.tree[1][obj].box_coordinates[1]+self.tree[1][obj].box_coordinates[3])/2)
                    x2=self.tree[1][c].box_coordinates[2]
                    y2=int((self.tree[1][c].box_coordinates[1]+self.tree[1][c].box_coordinates[3])/2)  
                self.draw.line((x1,y1,x2,y2), fill=self.line_color, width=self.line_thickness)       
    def __length_by_chars(self, obj):
        w=0
        for c in self.tree[1][obj].text:
            w+=self.tree[1][obj].font.getsize(c)[0]
        return w
    def __organize_by_rows_and_colums(self):
        for x in self.tree[0]:
            obj=self.tree[1][x]
            if not obj.row in self.__object_rows:
                self.__object_rows[obj.row]=[obj.name]
            else:
                self.__object_rows[obj.row].append(obj.name)
            if not obj.column in self.__object_columns:
                self.__object_columns[obj.column]=[obj.name]
            else:
                self.__object_columns[obj.column].append(obj.name)  
    def __check_is_consecutive(self, l):
            maximum = max(l)
            if sum(l) == maximum * (maximum+1) /2 : 
                return True
            return False    
    def __verify_rows_and_columns(self):
        nrow=[]
        ncolumn=[]
        for n in sorted(self.__object_rows):
            nrow.append(n)
        for n in sorted(self.__object_columns):
            ncolumn.append(n)
        if not self.__check_is_consecutive(nrow) or not self.__check_is_consecutive(ncolumn):
            raise Errors.ImproperLayerDeclaration  
        crds=[]
        for obj in self.tree[0]:
            if not (self.tree[1][obj].column, self.tree[1][obj].row) in crds:
                crds.append((self.tree[1][obj].column, self.tree[1][obj].row))
            else:
                raise Errors.ClashingCoordinates
    def __recognize_and_draw_shape(self, obj, iterator, objects):
        if self.tree[1][obj].cover=='rectangle':
            #self.draw.rectangle(xy=(int(iterator/(objects+1)*self.width)-self.tree[1][obj].font.getsize(self.tree[1][obj].text)-10, int(self.height/2)-4,int(iterator/(objects+1)*self.width)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[0]+10,int(self.height/2)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[1]+4),outline="black")
            x1=int((iterator/(objects+1))*self.width)-int(self.width/(self.width/40))
            x2=int((iterator/(objects+1))*self.width)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[0]
            y1=int(self.height/2)-self.height/(self.height/10)
            y2=int(self.height/2)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[1]+self.height/(self.height/10)
            self.tree[1][obj].box_coordinates=(x1,y1,x2,y2)
            self.draw.rectangle(xy=(x1,y1,x2,y2),outline=self.box_outline, fill=self.tree[1][obj].bgcolor)
    def add_object(self, obj):
        if isinstance(obj, NewObject):
            self.tree[0][obj.name]={}
            self.tree[1][obj.name]=obj
        else:
            raise Errors.InvalidObject
    def render(self):
        objects=len(self.tree[0])
        iterator=0
        self.__organize_by_rows_and_colums()
        self.__verify_rows_and_columns()
        print(self.__object_rows)
        for obj in self.tree[0]:
            iterator+=1
            self.tree[1][obj].coordinates=(int(int(float(iterator/(objects+1))*self.width)-int(self.width/((1/20)*self.width))), int((1/2)*self.height))
            self.__recognize_and_draw_shape(obj, iterator, objects)       
            self.draw.text(self.tree[1][obj].coordinates, self.tree[1][obj].text, self.tree[1][obj].textcolor, font=self.tree[1][obj].font)
        for obj in self.tree[0]:
            self.__connect_objs(obj)

                    
        return self.canvas

class Errors:
    class InvalidObject(Exception):
        """Raised when the object passed is not of the correct type"""
        def __init__(self, message="The object passed was not of the correct type"):
            self.message=message
        def __str__(self):
            return str(self.message)
    class ObjectNotInTable(Exception):
        """Raised when the object passed is not in a chart"""
        def __init__(self, message="The objects passed are not in a chart"):
            self.message=message
        def __str__(self):
            return str(self.message)
    class ImproperLayerDeclaration(Exception):
        """Raised when either the rows or columns declared have empty gaps in them"""
        def __init__(self, message="Rows or columns specified have a difference larger than 1"):
            self.message=message
        def __str__(self):
            return str(self.message)
    class ClashingCoordinates(Exception):
        """Raised when 2 objects have the same row and same column"""
        def __init__(self, message="2 objects in the table have the same row and same column"):
            self.message=message
        def __str__(self):
            return str(self.message)
