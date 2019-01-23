data = csvread("data_01232019_111919.txt")

time = data(:,1)

payload_x =  data(:,2)
payload_y =  data(:,3)
payload_z =  data(:,4)

plot(time,payload_x)
hold on;
plot(time,payload_y)
plot(time,payload_z)