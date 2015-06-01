function [gama,theta]=tran(x,y)
    gama=sqrt(x*x+y*y);
    theta=atan(y/x);