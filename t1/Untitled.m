data=imread('g.jpg');%imshow(data);
data=double(data);

for i=600:1200
    for j=1400:1600
        data(i,j,:)=data(1300,1600,:);
    end
end
data=uint8(data);
imwrite(data,'re.png');