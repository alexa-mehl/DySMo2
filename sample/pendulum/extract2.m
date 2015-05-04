function [dataNames, data] = extract2(yout)

yout.unpack('all')
clear yout
dataNames = who;
for i=1:length(dataNames)
    data(:,i) = eval([dataNames{i},'.Data']);
    
end


data(:,end+1) = eval([dataNames{i},'.Time']);
dataNames{end+1} = 'Time'