from BezierCurve import BezierCurve
from random import uniform
from selenium import webdriver
import time

class MouseMover:

    def __init__(self, driver):
        self.driver = driver

    def move_mouse_bezier_curve(self):
        list_of_points = [(uniform(1.1, 1.5),uniform(1.1, 1.9)),(uniform(3.5,3.8),uniform(5, 5.6)), (uniform(5, 5.5),uniform(3.7,4.1))]

        bezier_curve = BezierCurve(list_of_points)
        curve_plot_points = bezier_curve.plot_curve()
        
        num_of_plots = 0
        for plot_point in curve_plot_points:
            if num_of_plots % 10 == 0:
                x_plot = plot_point[0]
                y_plot = plot_point[1]
                webdriver.ActionChains(self.driver).move_by_offset(x_plot, y_plot).perform()

            num_of_plots = num_of_plots + 1

        
    
        
    
        