from manim import *

class SimpleScene(ThreeDScene):
    def construct(self):

        text = MarkupText(
            '<span foreground="yellow">Hello</span>, <span foreground="red"><i>Manim</i></span>!',
            font="Arial",
            font_size=72
        )
        

        circle = Circle()  # Create a circle
        circle.set_fill(PINK, opacity=0.5)  # Set the fill color and opacity
        circle.set_stroke(BLUE, width=4)  # Set the stroke color and width
        
        square = Square()  # Create a square
        square.set_fill(GREEN, opacity=0.5)  # Set the fill color and opacity

        # 将摄像头设为3D视角
        self.set_camera_orientation(theta=0*DEGREES, phi=0*DEGREES)
        vector = circle.get_center()
        side_length = 2
        cube = Cube(side_length=side_length)  # Create a cube
        cube.set_shading(True)  # Enable shading for better 3D effect
        cube.set_color(GREEN)    # Set the color of the cube
        # Position the cube above the circle along the z-axis by half the cube's side length
        cube.move_to(vector + OUT * (side_length / 2)) # type: ignore

        self.play(Create(circle))  # Animate the creation of the circle
        self.play(Transform(circle, square))  # Transform the circle into a square

        # circle 被就地变形为正方形，所以接下来的操作应作用在 circle 上

        self.play(Rotate(circle, angle=PI/2))  # Rotate the displayed square by 45 degrees
        
        # Cube 不是 VectorizedMobject，不能用 ReplacementTransform

        # 改为同时淡出平面对象并淡入立方体，设置不同速度和缓动：
        self.play(
            FadeOut(circle, run_time=0.2, rate_func=smooth),
            FadeIn(cube, run_time=0.6, rate_func=smooth),
        )
        self.play(Rotate(cube, angle=PI/4, axis=UP, rate_func=smooth))  # Rotate the cube around the UP axis
        self.move_camera(theta=PI/6, phi=PI/2)  # Change camera view

        self.play(FadeOut(cube))  # Uncreate the displayed square

        self.move_camera(theta=0*DEGREES, phi=-180*DEGREES)
        
        self.add_fixed_in_frame_mobjects(text)
        self.play(Write(text))  # Write the text on the screen

        self.wait(1)  # Wait for a second