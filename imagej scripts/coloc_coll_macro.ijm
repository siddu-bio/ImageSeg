function colocFunct(neuronsize,nscale,d,c1,c2,c3,c4)
{
open(d);
p = 5; //p designates the number of puncta to be collected per image
close();
for(i = 0; i < p; i++){

       open(d);
       run("Split Channels");
       selectWindow(c1);
       close();
       selectWindow(c4); //closes window for neun with bad data
       close();
       selectWindow(c3);//change the following select if general marker channel is not channel 3
       run("Scale Bar...", "width=["+nscale+"] height=4 font=14 color=White background=None location=[Lower Left] bold overlay");
       run("Maximize");
       waitForUser;
       run("Enhance Contrast", "saturated=0.1");//increases contrast and saturation may not be needed
       run("Apply LUT");
       run("JACoP ", "imga=["+c2+"] imgb=["+c3+"] pearson");
       close(c2);
       close(c3);
       close(c4);
       print("Neuron Size:"+neuronsize+"");
       }
}

//large (45?51 microns)
//medium (33?38 microns)
//small (20?27 microns) 

one = "C1-"
two = "C2-"
three = "C3-"
four = "C4-"
ttl = getTitle()
dir = getDirectory("image")
chan1 = one+ttl
chan2 = two+ttl
chan3 = three+ttl
chan4 = four+ttl
dtry = dir+ttl


colocFunct("Big Neurons",50,dtry,chan1,chan2,chan3,chan4)

colocFunct("Medium Neurons",35,dtry,chan1,chan2,chan3,chan4)

colocFunct("Small Neurons",25,dtry,chan1,chan2,chan3,chan4)

close();

selectWindow("Log");
