from __future__ import annotations
import configparser
import copy
import json
import logging
from typing import TYPE_CHECKING

from rich import color, errors
from rich import print as printf
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from manim import *
import math

from manim.utils.family_ops import extract_mobject_family_members
from pauseandthink import PauseAndThink
class DisplayP(ThreeDScene):
    
    def renderps(self, n ):
            rectangles = []
            for r in np.arange(0, 1 + 1/n, 1/n):
                h = 2 + 2 * math.sqrt(2)
                recb = 2 * math.sqrt(1 - r**2)
                base = math.sqrt(2)*recb
                nr = 1-recb/2
                c1 = ((h/2-nr) + (h/2-2*math.sqrt(2)-nr))/2
                c2 = (-(h/2)+2*math.sqrt(2)+nr +  -h/2+nr)/2
    
                f1 = c1 + base/2
                f2 = c2 + base/2
                f3 = c2 - base/2
                f4 = c1 - base/2
    
    
    
                nh = h-2*r
              
                f = Polygon([-recb/2, f1, r],[recb/2, f2 , r],[recb/2,  f3, r],[-recb/2,  f4,   r], color=RED)
                vertices = f.get_vertices()
                for vertex in vertices:
                    adjusted_vertex = vertex + np.array([0, 0, 0.05])  # Add 0.05 to the z-coordinate
                    dot = Dot(point=adjusted_vertex, radius=0.06, color=WHITE)
                    self.add(dot)
        
                # Extrude the polygon
                prism = self.extrude(f, height=1/n, scene=self)
                logger.info(str(prism))
                # Wait for a short time before the next step
                rectangles.append(prism)
                self.wait(0.1)

            return rectangles

    def render_pause_and_think(self):
        # Directly recreate PauseAndThink scene animations
        pause_logo = Line(start=LEFT, end=RIGHT, stroke_width=10)
        pause_logo.shift(UP)
        
        text = Text("Pause and Think", font_size=36)
        text.next_to(pause_logo, DOWN)

        self.play(Write(pause_logo), Write(text))
        self.wait(5)


    def extrude(self, polygon, height, scene):
        # Get the vertices of the polygon
        vertices = polygon.get_vertices()
        
        # Create the top face by moving the vertices up by the height
        top_face = [vertex + np.array([0, 0, height]) for vertex in vertices]

        # Create the side faces and the top face
        side_faces = []
        for i in range(len(vertices)):
            next_i = (i + 1) % len(vertices)
            side_face = Polygon(
                vertices[i], vertices[next_i], top_face[next_i], top_face[i],
                fill_opacity=0.5, color=BLUE
            )
            side_faces.append(side_face)

        # Combine the top face and side faces into a single 3D object
        extruded_shape = VGroup(
            Polygon(*top_face, fill_opacity=0.7, color=RED),
            *side_faces
        )

        # Add the extruded shape to the scene
        scene.add(extruded_shape)

        return extruded_shape


    def construct(self):
        # Calculate the height of the rectangle
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        h = 2 + 2 * math.sqrt(2)

        blue_hex = "#58C4DD"
        green_hex = "#83C167"

        # Convert hex to RGB manually
        blue_rgb = [
            int(blue_hex[1:3], 16),  # Red component
            int(blue_hex[3:5], 16),  # Green component
            int(blue_hex[5:7], 16)   # Blue component
        ]
        green_rgb = [
            int(green_hex[1:3], 16),  # Red component
            int(green_hex[3:5], 16),  # Green component
            int(green_hex[5:7], 16)   # Blue component
        ]
        angle_radians = math.radians(45)
        # Mix the colors by averaging their RGB values
        mixed_rgb = [
            int((b + g) / 2) for b, g in zip(blue_rgb, green_rgb)
        ]

        # Convert mixed RGB values back to hex
        mixed_hex = "#{:02x}{:02x}{:02x}".format(mixed_rgb[0], mixed_rgb[1], mixed_rgb[2])

        # Use the mixed hex color in Manim
        mixed_color = ManimColor(mixed_hex)





        # Create two rectangles with the same dimensions
        rectangle = Rectangle(width=2, height=h, fill_color=BLUE, fill_opacity=0.5)
        rectangle2 = Rectangle(width=2, height=h, fill_color=GREEN, fill_opacity=0.5)
        end_point = rectangle2.get_corner(DR) + np.array([
            -h * math.cos(angle_radians),  # Move left (negative x)
            h * math.sin(angle_radians),   # Move up (positive y)
            0                                   # z-coordinate (assuming 2D plane)
        ])

        diagonal=  Line(rectangle2.get_corner(DR), end_point )
        # Center the rectangles on the screen
        rectangle.move_to(ORIGIN)
        rectangle2.move_to(ORIGIN)

        # Add the first rectangle to the scene
        self.play(Create(rectangle), subcaption_duration=0.5)
       
        self.wait(0.5)

        # Add the second rectangle to the scene
        self.play(Create(rectangle2),subcaption_duration=0.5)
        self.wait(0.5)

        recl = Line(rectangle.get_corner(DL), rectangle.get_corner(DR))
        self.add(recl)

        # Create a second line that starts from the same point as recl but extends vertically
        new_end_point = rectangle.get_corner(DL) + UP * h
        recl2 = Line(rectangle.get_corner(DL), new_end_point)
        self.add(recl2)

        # Create braces and labels
        b1 = Brace(recl)
        labelrh =  MathTex("b = 2", font_size=36).next_to(b1,DOWN)

        self.play(Create(b1), Write(labelrh))

        # Ensure recl2 is visible before creating b2
        b2 = Brace(recl2, direction=LEFT)  # Direction RIGHT or direction=UP based on placement
        
        labelh1 = MathTex(r"h = 2 + 2 \cdot \sqrt{2}", font_size=36).next_to(b2,LEFT)
        

        # Add braces and labels to the scene
        self.play(Create(b2), Write(labelh1) )
        

        # Animate the rotation of the first rectangle with a shorter duration
        self.play(
            rectangle.animate.rotate(PI / 4),
            run_time=1  # Duration of 1 second for the rotation animation
        )
        
        
        base1 = Line(rectangle2.get_corner(DL), rectangle2.get_corner(DR))

       

        # Display the rectangles


        # Create the angle between the two bases
        angle = Angle(base1, diagonal, radius=0.5)

        # Add the angle to the scene
        

        supplementary_angle_radians = PI - angle.get_value()

        # Create the supplementary angle as an arc
        supplementary_arc = Arc(
            radius=0.5,
            start_angle=angle.get_value(),
            angle=supplementary_angle_radians,
            color=RED
        )

        # Position the supplementary arc horizontally
        
        supplementary_arc.shift(DOWN * 2.44)
        supplementary_arc.shift(RIGHT * 1)

        # Add the supplementary arc to the scene
        self.play(Create(supplementary_arc))

        # Optionally, label the angle
        angle_label = MathTex(r"45^{\circ}").next_to(angle, UP)
        angle_label.shift(LEFT * 0.7).shift(DOWN * 0.4)
        self.play(Write(angle_label))

        octagon = RegularPolygon(n=8, radius=2 / (2 * np.sin(PI / 8))).rotate(PI/8)  # n=8 for octagon
        octagon.set_stroke(width=3)  # Set line width

        braceline1 = Line([1+ math.sqrt(2), -1, 0], [1+ math.sqrt(2), 1, 0], color=BLUE)
        braceline2 = Line([1+ math.sqrt(2), -1, 0], [1+ math.sqrt(2), -1 - math.sqrt(2), 0], color=RED)
        braceline3 = Line([1+ math.sqrt(2), 1, 0], [1+ math.sqrt(2), 1 + math.sqrt(2), 0], color=GREEN)

        # Add lines to the scene
        dashed_octagon = DashedVMobject(octagon, num_dashes=16, color=WHITE)
        # Calculate lengths of the lines
        len_braceline1 = braceline1.get_length()
        len_braceline2 = braceline2.get_length()
        len_braceline3 = braceline3.get_length()

        # Create MathTex objects for the lengths and position them next to the lines (to the right)
        text_braceline1 = MathTex("2", font_size=36).next_to(braceline1, RIGHT)
        text_braceline2 = MathTex(r"\sqrt{2}", font_size=36).next_to(braceline2, RIGHT)
        text_braceline3 = MathTex(r"\sqrt{2}", font_size=36).next_to(braceline3, RIGHT)

        # Add the length labels to the scene
        self.play(Create(dashed_octagon))
        # Keep the scene for a bit
        self.wait(2)

        # Convert the solid line into a dashed line
        

        # Add the dashed octagon to the scene
        self.play(Create(dashed_octagon))
        self.play(Create(braceline1), Create(braceline2), Create(braceline3))
        self.play(Write(text_braceline1), Write(text_braceline2), Write(text_braceline3))


        # Keep the scene for a bit
        self.wait(5)

        everything = VGroup(rectangle, rectangle2, labelrh, labelh1, b1, b2 , recl, recl2, angle_label, supplementary_arc)
        self.remove(text_braceline1,text_braceline2,text_braceline3,octagon, braceline1, braceline2, braceline3, dashed_octagon)
        everything.shift(LEFT * 2.5)
        parallelogram1 = Polygon(
            [-3.5, h/2, 0], [-1.5 , h/2-2, 0], [-1.5,-h/2, 0], [-3.5, -(h/2-2), 0]
        )

        linehb = Line([-3.5, h/2, 0], [-3.5 , -(h/2-2), 0])
        linehp = Line([-3.5, -(h/2-2), 0], [-1.5 , -(h/2-2), 0])
        hb = Brace(linehb, direction=RIGHT)
        hp = Brace(linehp, direction=DOWN)

        labelhb = MathTex(r"b_p").next_to(hb, RIGHT)
        labelhp = MathTex(r"h_p").next_to(hp, DOWN)



        parallelogram = Polygon(
            [1, 0, 0], [1+2 * math.sqrt(2), 0, 0], [2 * math.sqrt(2), 2, 0], [0, 2, 0]
        )
        parallelogram.set_fill(mixed_color, opacity=0.5)        
        # Shift the parallelogram slightly to the left
               
        self.play(Create(parallelogram1), Create(hb), Create(hp), Write(labelhb), Write(labelhp))
        self.play(Transform(parallelogram1, parallelogram))
        line = Line(start=ORIGIN, end=[0, 2, 0])
        lineb = Line(start=ORIGIN, end=[2, 0, 0])
        # Create a label "h" and position it above the line
        
        parallelogram.shift(RIGHT * 2) 
        line.shift(RIGHT * 2)
        lineb.shift(RIGHT * 2)
        label = MathTex("h_p").next_to(line, UP)
        label2 = MathTex("b_p").next_to(lineb, DOWN).shift(LEFT* 0.3)


        areap = MathTex(r"A = h_p \cdot b_p", font_size=48)
        bp_eq = MathTex(r"b_p = h_p \cdot \sqrt{2}", font_size=48)
        areap.next_to(lineb, DOWN).shift(DOWN * 0.7)
        bp_eq.next_to(line, DOWN).shift(DOWN * 1.4).shift(RIGHT * 1.2)
        
        self.add(areap)
        self.add(bp_eq)
        # Add the line and the label to the scene
        self.play(Create(line))
        self.play(Write(label))
        self.play(Write(label2))
        self.wait(1)


        self.remove(parallelogram, line, lineb, label, label2, areap, labelrh, labelh1,  angle_label, supplementary_arc, b1, b2, parallelogram1, hb, hp, labelhb, labelhp, diagonal, base1, bp_eq)
        # Wait to see the 2D view before starting the rotation
        self.wait(1)
     
   
        everything.shift(RIGHT * 2.5)
        
        self.play(theta.animate.set_value(-225*DEGREES))#225
        self.play(phi.animate.set_value(60*DEGREES))

        # b = 2rsqrt(r)
        # h = 2*sqrt(1-r^2)


        self.wait(2)


        rectanglep = Prism(dimensions=[2, h, 0.1], fill_color=GREEN, fill_opacity=0.9)
        rectangle2p = Prism(dimensions=[2, h, 0.1], fill_color=BLUE, fill_opacity=0.9)


        r = ValueTracker(0)

        def updaterec(mob):
            recb = 2 * math.sqrt(1 - r.get_value()**2)
            mob.stretch_to_fit_width(recb)
            mob.stretch_to_fit_depth(r.get_value())
            mob.move_to([mob.get_center()[0], mob.get_center()[1], r.get_value() ])
        
        def updaterec2(mob):
            anrec = Polygon([-1,h/2,0],[-1,-h/2,0],[1,-h/2,0],[1,h/2,0], fill_color=BLUE, fill_opacity=0.7)
       
            recb = 2 * math.sqrt(1 - r.get_value()**2)
            anrec.stretch_to_fit_width(recb)
            anrec.stretch_to_fit_depth(r.get_value())
            anrec.move_to([anrec.get_center()[0], anrec.get_center()[1], r.get_value()])

            mob.become(anrec)
            mob.rotate(PI/4, axis=OUT)


            anrec.clear_updaters()
            anrec.remove()


        def updatepar(mob):
            h = 2 + 2 * math.sqrt(2)
            recb = 2 * math.sqrt(1 - r.get_value()**2)
            base = math.sqrt(2)*recb
            nr = 1-recb/2
            c1 = ((h/2-nr) + (h/2-2*math.sqrt(2)-nr))/2
            c2 = (-(h/2)+2*math.sqrt(2)+nr +  -h/2+nr)/2

            f1 = c1 + base/2
            f2 = c2 + base/2
            f3 = c2 - base/2
            f4 = c1 - base/2



            nh = h-2*r.get_value()
          
            f = Polygon([-recb/2, f1, r.get_value()],[recb/2, f2 , r.get_value()],[recb/2,  f3, r.get_value()],[-recb/2,  f4,   r.get_value()], color=BLACK)
            mob.become(f)
            mob.move_to([mob.get_center()[0], mob.get_center()[1], r.get_value() ])
       
        


            
            

       
            
        rectanglep.move_to(ORIGIN)
        rectangle2p.move_to(ORIGIN).rotate(PI/4, axis=OUT)
        
        


        # Create a 3D axes and a cylinder
        axes = ThreeDAxes()
        labels = axes.get_axis_labels(
            Text("X").scale(0.7), Text("Y").scale(0.45), Text("Z").scale(0.45)
        )
        self.add(axes, labels)
        cylinder = Cylinder(radius=1, height=h, direction= [0,1,0], fill_color=GREEN, fill_opacity=0.2)
        cylinder2 = Cylinder(radius=1, height=h, direction= [-1,1,0], fill_color=BLUE, fill_opacity=0.2)
        cylinder.set_stroke(GREEN)
        cylinder.set_stroke(BLUE)
        # Add the cylinder to the scene
        self.play(Create(cylinder))
        self.play(Create(cylinder2))
        self.wait(1)

        rectanglep.add_updater(updaterec)
        rectangle2p.add_updater(updaterec2)

        # Add rectangles to the scene
        
        
        self.play(Create(rectangle2p))
        self.play(Create(rectanglep))

        # Animate the change in r
        
    
        ## Clean up updaters after the animation
        #rectangle.clear_updaters()
        #rectangle2.clear_updaters()
        parallelogram2 = Polygon(
            [1, 0, 0], [1+2 * math.sqrt(2), 0, 0], [2 * math.sqrt(2), 2, 0], [0, 2, 0]
        )
        self.add(parallelogram2)

        r = ValueTracker(0)
        parallelogram2.add_updater(updatepar)
    
        self.play(r.animate.set_value(1), run_time=5, rate_func=linear)
        rectss = self.renderps(n=10)
        self.wait(1)
        logger.info("rectangles:")
        logger.info(repr(rectss))
        for i in rectss:
            self.remove(i)
            self.wait(0.05)
        self.wait(1)
       
        rectss = self.renderps(n=20)
        self.play(distance_to_origin.animate.set_value(1.7), run_time=0.5)  
        self.play(theta.animate.set_value(-270 * DEGREES), run_time=0.5)  
        self.play(phi.animate.set_value(89 * DEGREES), run_time=0.5) 

        
        self.wait(1)
        drline = Line([-1, h/2, 0.4],[1.1, h/2, 0.4] , color = WHITE, stroke_width=3)
        drline2 = Line([-1, h/2, 0.45],[1.1, h/2, 0.45] , color = WHITE, stroke_width=3)
        linesss = VGroup(drline, drline2)
        self.play(Create(linesss) )
        dh_text = MathTex(r"dh", color=WHITE, font_size=28)
        dh_text.rotate(PI / 2, axis=RIGHT)
        dh_text.rotate(PI, axis=OUT)
        dh_text.move_to(axes.c2p(2.5, 0, 2))
        # Position the text to the right of the lines
        dh_text.next_to(drline2.get_end(), RIGHT)
        # Add the text to the scene
        self.play(Write(dh_text))
        self.wait(3)
        self.remove(dh_text,linesss)
        logger.info("rectangles:")
        logger.info(repr(rectss))
        for i in rectss:
            self.remove(i)
            self.wait(0.05)
        self.wait(1)
        
        integral = MathTex(r"V = 2 \int_{0}^{1} b_p(h) \cdot h_p(h) \, dh",  font_size=28)

        integral.rotate(PI / 2, axis=RIGHT)
        integral.rotate(PI, axis=OUT)
        integral.move_to(axes.c2p(2.5, 0, 2))

        # Add the axes and the integral to the scene
        
       
        self.play(Write(integral))

        hv = ValueTracker(0)

        hline = Line([0, h/2, 0],[0, h/2, 0.05] , color = YELLOW, stroke_width=3)
        baseline = Line([-1, h/2, 0],[1, h/2, 0.05], color = RED, stroke_width=3 )
        rline = Line([0, h/2, 0],[1, h/2, 0], color = GREEN)
        brace_hline = Brace(hline, color=BLUE)
       
        # Create text labels for braces
        text_hline = MathTex(r"h = {:.2f}".format(hline.get_length()), color = YELLOW ,font_size=18)
        text_baseline = MathTex(r"h_p(h) = {:.2f}".format(baseline.get_length()), color=RED,font_size=15)
        text_rline= MathTex(r"r=1", color = GREEN ,font_size=18)

        text_hline.rotate(PI / 2, axis=RIGHT)
        text_hline.rotate(PI, axis=OUT)
        text_baseline.rotate(PI / 2, axis=RIGHT)
        text_baseline.rotate(PI, axis=OUT)
        text_rline.rotate(PI / 2, axis=RIGHT)
        text_rline.rotate(PI, axis=OUT)
        
        text_hline.next_to(hline, OUT)
        text_baseline.next_to(baseline, OUT)
        
        self.add(hline, baseline, rline)
        # Add braces and text to the scene
        self.add( text_hline, text_baseline)

        def updateh(mob):
            mob.become(Line([0, h/2, 0], [0, h/2, hv.get_value()], color=YELLOW,stroke_width=3 ))
            
            # Create and scale the brace for h
            
            # Update the text for h and shift it slightly towards the negative x-axis
            text_hline.become(MathTex(r"h = {:.2f}".format(mob.get_length()), color=YELLOW, font_size=18))
            rline.become(Line([0, h/2, 0], [math.sqrt(1 - hv.get_value()**2), h/2, hv.get_value()], color=GREEN,stroke_width=3 ))
            text_hline.rotate(PI / 2, axis=RIGHT)
            text_hline.rotate(PI, axis=OUT)
            text_hline.next_to(mob, UP)
            
            # Shift the text_hline towards the negative x-axis
            text_hline.shift(LEFT * 0.5)

        def updathp(mob):
            mob.become(Line([math.sqrt(1 - hv.get_value()**2), h/2, hv.get_value()],
                            [-math.sqrt(1 - hv.get_value()**2), h/2, hv.get_value()], color=RED, stroke_width=3))
        
            # Create and scale the brace for h_p(h)
            # Update the text for h_p(h)
            text_baseline.become(MathTex(r"h_p(h) = {:.2f}".format(mob.get_length()), color=RED, font_size=15))
            text_baseline.rotate(PI / 2, axis=RIGHT)
            text_baseline.rotate(PI, axis=OUT)
            text_baseline.next_to(mob, OUT)
            text_rline.next_to(rline, OUT)
           
            text_baseline.shift( -OUT*0.2)


        hline.add_updater(updateh)
        baseline.add_updater(updathp)
        self.remove(rectangle, rectangle2p, rectangle2, parallelogram2, rectanglep, recl )
        circA = Circle(radius=1, color=BLACK)
        circA.rotate(PI / 2, axis=RIGHT)
        # Move the circle to the correct position on the Y-axis
        circA.move_to([0, h/2, 0]) 
        self.play(Create(circA))
        self.wait(1)
        self.play(hv.animate.set_value(1), run_time=8, rate_func=linear)
        # Keep the final scene displayed for a few seconds

        equation_1 = MathTex(r"\left(\frac{h_p(h)}{2}\right)^2 + h^2 = 1", font_size= 28)
        

        # Display the steps of solving for h_p:
        step_1 = MathTex(r"\left(\frac{h_p(h)}{2}\right)^2 = 1 - h^2", font_size= 28)
        step_2 = MathTex(r"\frac{h_p(h)}{2} = \sqrt{1 - h^2}", font_size= 28)
        step_3 = MathTex(r"h_p(h) = 2\sqrt{1 - h^2}", font_size= 28)

        # Apply rotation to make text visible in the correct plane
        for tex in [equation_1, step_1, step_2, step_3]:
            tex.rotate(PI / 2, axis=RIGHT)  # Rotate 90 degrees around the X-axis
            tex.rotate(PI, axis=OUT) 
            tex.shift(2*LEFT)  
            tex.shift(1.5*OUT)      # Rotate 180 degrees around the Z-axis

        # Position the equations
        equation_1.to_edge(UP)
        step_1.next_to(equation_1, DOWN, buff=0.5)
        step_2.next_to(step_1, DOWN, buff=0.5)
        step_3.next_to(step_2, DOWN, buff=0.5)

        # Animations to display equations step by step
        self.play(Write(equation_1))
        self.wait(2)

        # Transform the first equation to the next step
        self.play(Transform(equation_1, step_1))
        self.wait(2)

        # Continue with the next step
        self.play(Transform(equation_1, step_2))
        self.wait(2)

        # Derive the final equation
        self.play(Transform(equation_1, step_3))
        self.wait(2)


        updated_integral = MathTex(r"V = 2 \int_{0}^{1} b_p(h) \cdot 2\sqrt{1 - h^2} \, dh", font_size=28)
        updated_integral.rotate(PI / 2, axis=RIGHT)  # Rotate 90 degrees around the X-axis
        updated_integral.rotate(PI, axis=OUT) 
        updated_integral.shift(2*RIGHT)  
        updated_integral.shift(1.5*OUT)    

        self.play(Transform(integral, updated_integral))
        self.wait(10)
        bp_e2 = MathTex(r"b_p(h) = h_p(h) \cdot \sqrt{2}", font_size=28)
        bp_e2.rotate(PI / 2, axis=RIGHT)  # Rotate 90 degrees around the X-axis
        bp_e2.rotate(PI, axis=OUT) 
        bp_e2.shift(2*LEFT)  
        bp_e2.shift(1.5*OUT)  
        
        self.stop_ambient_camera_rotation(about='theta')

        self.remove(equation_1)
        self.play(Write(bp_e2))
        updated_integral2 = MathTex(r"V = 2 \int_{0}^{1} h_p(h) \cdot \sqrt{2} \cdot 2\sqrt{1 - h^2} \, dh", font_size=24)
        updated_integral3 = MathTex(r"V = 2 \int_{0}^{1} 2\sqrt{1 - h^2} \cdot \sqrt{2} \cdot 2\sqrt{1 - h^2} \, dh", font_size=24)
        updated_integral4 = MathTex(r"V = 2 \int_{0}^{1} 4  \cdot \sqrt{2} \cdot (1-h^2), dh", font_size=24)
        updated_integral5 = MathTex(r"V = 8 \cdot \sqrt{2} \int_{0}^{1} 1-h^2, dh", font_size=24)
        for tex in [updated_integral2, updated_integral3, updated_integral4, updated_integral5]:
            tex.rotate(PI / 2, axis=RIGHT)  # Rotate 90 degrees around the X-axis
            tex.rotate(PI, axis=OUT) 
            tex.shift(2*RIGHT)  
            tex.shift(1.5*OUT)    

        self.play(Transform(integral, updated_integral2))
        self.wait(2)
        self.play(Transform(integral, updated_integral3))
        self.wait(2)
        self.play(Transform(integral, updated_integral4))
        self.wait(2)
        self.play(Transform(integral, updated_integral5))

def main():
    # Set the log level to show all messages (optional)
    logger.setLevel("DEBUG")

    # Create an instance of the DisplayP class and run the scene
    scene = DisplayP()
    scene.render()

    # Print a message to the console

if __name__ == "__main__":
    main()

   



       
