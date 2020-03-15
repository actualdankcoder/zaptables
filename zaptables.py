from PIL import Image, ImageDraw, ImageFont
import random
class NewObject:
    def __init__(self, name="OBJECT"+str(random.randint(10000,99999)),text="OBJECT",cover=ObjectTypes.Rectangle(), layer=1, bgcolor=(255,255,255),textcolor=(0,0,0),font=('cg.ttf', 20)):
        self.layer=layer
        self.name=name
        self.text=text
        self.bgcolor=bgcolor
        self.textcolor=textcolor
        self.font=ImageFont.truetype(font[0],font[1])
        self.cover=cover
class ObjectTypes:
    class Rectangle:
        pass
    class RoundedRectangle:
        pass
    class Sphere:
        pass

class Chart:
    def __init__(self, width, height,background=(255,255,255)):
        self.width=width
        self.height=height
        self.canvas=Image.new('RGB',(self.width, self.height), background)
        self.draw=ImageDraw.Draw(self.canvas)
        self.tree=({},{})
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
        return self.canvas
class Errors:
    class InvalidObject(Exception):
        """Raised when the object passed is not of the correct type"""
        def __init__(self, message="The object passed was not of the correct type"):
            self.message=message
        def __str__(self):
            return str(self.message)