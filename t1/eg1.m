function f=out(a,b,c)
if nargin==1
    f=a;
elseif nargin==2
    f=a+b;
elseif nargin==3
    f=a*b*c*2;
end