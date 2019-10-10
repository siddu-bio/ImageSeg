one = "C1-"
two = "C2-"
three = "C3-"
four = "C4-"
merge = "Composite"
ttl = getTitle()
dir = getDirectory("image")
channel1 = one+ttl
channel2 = two+ttl
channel3 = three+ttl
channel4 = four+ttl
directory = dir+ttl
function colocFunct(neuronsize,d,c1,c2,c3,c4)
{
i = 1;
p = 5; //p designates the number of puncta to be collected per image
close();
print(neuronsize)
for(i = 0; i < p; i++){
       setBatchMode(false);
       open(d);
       run("Split Channels");
       selectWindow(c1);
       close();
       selectWindow(c2);
       selectWindow(c3);
       selectWindow(c4);
       selectWindow(c3);//change the following select if general marker channel is not channel 3
       run("Scale Bar...", "width=50 height=4 font=14 color=White background=None location=[Lower Left] bold overlay");
       waitForUser;
       run("Enhance Contrast", "saturated=0.1");//increases contrast and saturation may not be needed
       run("Apply LUT");
       run("JACoP ", "imga=["+c2+"] imgb=["+c3+"] pearson");
       close(c2);
       close(c3);
       close(c4);
       }       
}

//large (45‐51 microns)
//medium (33‐38 microns)
//small (20‐27 microns) 

colocFunct("Big Neurons",directory,channel1,channel2,channel3,channel4)

colocFunct("Medium Neurons",directory,channel1,channel2,channel3,channel4)

colocFunct("Small Neurons",directory,channel1,channel2,channel3,channel4)

selectWindow("Log");