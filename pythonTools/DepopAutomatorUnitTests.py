from EmailHelper import EmailHelper
from BezierCurve import BezierCurve
from random import uniform

def test_email():
    subject = "Email Test"
    message = "This is a message sent with email helper"
    
    email_helper = EmailHelper(subject, message, "mwspencer75@gmail.com")
    email_helper.send_message()

def test_bezier_curve():
    list_of_points = [(uniform(1.1, 1.5),uniform(1.1, 1.9)),(uniform(3.5,3.8),uniform(5, 5.6)), (uniform(5, 5.5),uniform(3.7,4.1))]
    bezier_curve = BezierCurve(list_of_points)
    bezier_curve_points = bezier_curve.plot_curve()
    return bezier_curve_points


def main():
    #test_email()
    list_of_points = test_bezier_curve()
    print(list_of_points)

    # BezierCurve([(1, 2), (3, 5)]).plot_curve()  # degree 1
    # BezierCurve([(0, 0), (5, 5), (5, 0)]).plot_curve()  # degree 2
    # BezierCurve([(0, 0), (5, 5), (5, 0), (2.5, -2.5)]).plot_curve()  # degree 3

main()     