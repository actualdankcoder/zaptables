from PIL import Image, ImageDraw, ImageFont
import random
class NewObject:
    def __init__(self, name="OBJECT"+str(random.randint(10000,99999)),text="OBJECT",cover='rectangle', layer=1, bgcolor=(255,255,255),textcolor=(0,0,0),font=('cg.ttf', 20)):
        self.layer=layer
        self.name=name
        self.text=text
        self.bgcolor=bgcolor
        self.textcolor=textcolor
        self.font=ImageFont.truetype(font[0],font[1])
        self.cover=cover

class Chart:
    def __init__(self, width, height,background=(255,255,255)):
        self.width=width
        self.height=height
        self.canvas=Image.new('RGB',(self.width, self.height), background)
        self.draw=ImageDraw.Draw(self.canvas)
        self.tree=({},{})
    def __length_by_chars(self, obj):
        w=0
        for c in self.tree[1][obj].text:
            w+=self.tree[1][obj].font.getsize(c)[0]
        return w
    def __recognize_and_draw_shape(self, obj, iterator, objects):
        if self.tree[1][obj].cover=='rectangle':
            #self.draw.rectangle(xy=(int(iterator/(objects+1)*self.width)-self.tree[1][obj].font.getsize(self.tree[1][obj].text)-10, int(self.height/2)-4,int(iterator/(objects+1)*self.width)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[0]+10,int(self.height/2)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[1]+4),outline="black")
            x1=int((iterator/(objects+1))*self.width)-int(self.width/(self.width/40))
            x2=int((iterator/(objects+1))*self.width)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[0]
            y1=int(self.height/2)-self.height/(self.height/10)
            y2=int(self.height/2)+self.tree[1][obj].font.getsize(self.tree[1][obj].text)[1]+self.height/(self.height/10)
            self.draw.rectangle(xy=(x1,y1,x2,y2),outline='black')
    def add_object(self, obj):
        if isinstance(obj, NewObject):
            self.tree[0][obj.name]={}
            self.tree[1][obj.name]=obj
        else:
            raise Errors.InvalidObject
    def render(self):
        objects=len(self.tree[0])
        iterator=0
        for obj in self.tree[0]:
            iterator+=1
            self.draw.text((int(int(float(iterator/(objects+1))*self.width)-int(self.width/((1/20)*self.width))), int((1/2)*self.height)), self.tree[1][obj].text, self.tree[1][obj].textcolor, font=self.tree[1][obj].font)
            self.__recognize_and_draw_shape(obj, iterator, objects)
        return self.canvas

class Errors:
    class InvalidObject(Exception):
        """Raised when the object passed is not of the correct type"""
        def __init__(self, message="The object passed was not of the correct type"):
            self.message=message
        def __str__(self):
            return str(self.message)
