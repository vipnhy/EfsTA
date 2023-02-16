# **EfsTA User Guide**

In this user guide the evaluation of femtosecond transient absorption spectra data using the program EfsTA will be explained.

This TA-Evaluation program allows the optimizing of the decay constants based on given values. These values should be derived of the 2D-data and previous knowledge of the photophysics of the molecule.

You can decide between using the graphical user-interface or the script form *App.py* in Python. They both have the features for the evaluation (GLA -> DAS and GTA -> SAS), as well as the plotting. However the UI checks for the completeness of the user inputs, whereas the script allows more customization.

## GUI

### Introduction

Upon starting the program the following window will popup. 

<img src="/images/GUI/Introduction.png" width="50%"/>

On this first tab a brief explanation of the program can be seen, which references this guide and provides contact information. There is also a possibility to change the theme of the GUI.

### Data

The GUI is designed to guide the user through an evaluation by going for tab to tab. Switching from the Introduction-tab to the Data-tab. The following will be seen.

<img src="/images/GUI/Data.png" width="50%"/>

Here the evaluation process starts. The first step is to provide the program with the directory, where the data for the evaluation is located. To provide the data simply copy and past the directory in the designated text field or click the Browse-Button to choose the directory via a directory dialog.

Note that the program only recognizes data in the form of three separate .txt-files for the wavelengths, delays and measured absorption ending with lambda.txt,delay.txt and spectra.txt respectively. 

If a directory is selected which was previously use to evaluate data the inputs made for the previous evaluation will be restored. To clear out all these inputs in case completely different parameters should  be used, the Clear Cache-Button will delete all inputs.

If the directory is a new one with a fresh set of data all input fields will be empty. The data can be shaped if required. The wavelength and time domain can be specified by providing upper and lower limits e.g. if artifacts around time 0 are a problem the lower bound for the delay values can be set to 0.4, so that only the data starting from 0.4 ps will be used. Additionally if the data was meassured in ODU but should be displayed as mOUD a data multiplier can be set e.g. 1000. These parameters are all optional and can be left empty.

After providing the data and shaping it the next step is to decide if the data should be analysed using global liftime analysis or global target analysis. Typically the first step is to use global lifetime analysis.

### Global Lifetime Analysis (GLA)

Going to the GLA-tab the following will be seen.

<img src="/images/GUI/GLA.png" width="50%"/>

Utilizing this model the spectrum will be treated as a collection of multiple parallel expoential decays.

First of the GLA-Button needs to be clicked, so that the program knows to use this model for the evaluation.
After that lifetimes for the different species need to be set, since this program relies on initial guesses by the user. A priori knowlegde or guesses about the amount of forming species during the irradiation and an approximate lifetime for each species is necessary. All lifetimes input need to be separated by a comma and depending on if they are to be optimized need to be input in the variable or fixed text fields respectively.

If the measured photochemical process involves for example the different species with two of them having lifetimes in the lower picosecond range and the third having a lifetime greater than the timeframe of the proccess. The two picosecond lifetimes should be input as variable lifetime values and the longer one as a fixed value since it does not contribute in a meaningful way to the spectrum.????

Lastly for the minimization of the Chi-Square-function different algorithms can be selected where the local minimizer Nelder-Mead is the standard but there are also global options with ampgo and basinhoppin which will take a bit longer.

If even more a priori knowledge is available global target analysis can be used.

### Global Target Analysis (GTA)

Going to the GTA-tab the following can be seen.

<img src="/images/GUI/GTA.png" width="50%"/>

Here the kinetic models on which the analysis is based can be input in three different ways. 

**Preset Models**

Firstly via the option "Preset Model" one of eight preimplemented kinectic models can be selected for the analysis. The available models are as follows.

The first two models are generic consecutive models with no branching.

- *Model 1* A generic consecutive model with no spefic limitation for the amount of species. In this model the last species will decay back to the ground state.

- *Model 2* A generic consecutive model with no spefic limitation for the amount of species. In this model the last species will **not** decay back to the ground state.

The last six models are consecutive models for a set amount of species with branching processes.

- *Model 3* A -> B -> C -> D; B -> D

- *Model 4* A -> B -> C -> D -> E; B -> E

- *Model 5* A -> B -> C -> D -> E; C -> E

- *Model 6* A -> B -> C -> D -> E -> F; C -> F

- *Model 7* A -> B; A -> C

- *Model 8* A -> B ; B -> C ; B -> D

After selecting a model the lifetimes for the species need to be set. For each transition or "->" there has to be one lifetime. So for Model 3 four lifetimes are required. Optionally for each of these lifetimes bounds can be set, so that during the optimization the values stay inside of a certain interval. If for example there are three lifetimes but the last one should never go below 200 the input for the lower bounds would be ",,200". Since the first two lifetimes don't need a lower limit they will be left empty and separated by a comma. The same goes for the input of the upper bounds.

**Custom Models**

Should the eight provided models not suffice the option "Custom Model" can be selected. This option allows the user to input their own kinetic model just by providing the program with a "reaction equation". The input for the equation should look as follows.

The custom models are limited to a maximum of 26 species. Each species needs to be denoted with a capital letter from A to Z. If one species decays back to the ground state the non capital letter v (for void) may be used. A decay into the ground state only has to be declared once per species. The equation can be written with arrows (A->B->C->v) or for faster input without the arrows (ABCv). The important thing is to keep them in the order of the transitions. The letters need to be selected in alphabetical order. For example if there are only the species the letters used need to be A,B and C **not** F,X and Q. For branching or transitions back to previos species start a new subequation by separation with a ";". For example given the following transitions:

<img src="/images/reaction example.png" width="30%"/>

the input for the eqaution would be:

A->B->C->v;B->A;A->C or ABCv;BA;AC.

These custom models can be saved for later use or deleted if no longer of interest.

The input of the lifetimes and their bounds work in the same way they work for the "Preset Models".

**Custom Matrix**

Lastly for more advanced users it is also possible to input a transition matrix directly. For this select the "Custom Matrix" option and enter the size of the matrix. The size corresponds to the amount of species. After that click the Open Table-Button. A new window will pop up with a table where the lifetimes can be input directly.

<img src="/images/Table.png" width="30%"/>

Given the following transitions:

<img src="/images/reaction example.png" width="30%"/>

the input for the matrix should look like this:

<img src="/images/matrix example.png" width="30%"/>

The matrix can be divided in three major parts. The main diagonal, the triangle above the main diagonal and the triangle below it. On the main diagonal the loss or decay of the corresponding species is described. The upper triangle describes the regain or repopulation of previous species. The lower triangle describes the gain or population of following species.

More specific the positions in the matrix always describe the relationship or rather the dependance of the species in the row from the species in the column. For example the position highlighted in blue in the upper triangle describes the dependence of species B from species C. The "reaction equation" shows that there is no transition from species C back to species B so the position is left empty or the input is zero. The position highlighted in red on the main diagonal shows the decay of species A. In the "reaction equation" there are two transitions from species A to another species in other words two ways for species A to lose population. Once through a transition to species B which occurs after a lifetime of τ<sub>1</sub> and once through a transition directly to species C a lifetime of τ<sub>5</sub> so the overall decay of species A is described by the negative sum of those lifetimes, since the transitions result in loss of population.

After all inputs are made the matrix can be saved and in after setting the plotting details the program can be executed.

### Plotting

With the selection of the analysis method the last thing left to do is to select if the raw and or fitted data should be plotted. EfsTA provides a variety of different plots.

**Plot Choices**

- *Delay Slices (ΔA/λ)*: Specified slices through the time domain will be shown as a plot of the absorption change against the wavelengths. (Will only be shown if delays are provided.)

<img src="/images/example plots/ex_timeslice.png" width="30%"/>

- *Wavelength Slices (t/ΔA)*: Specified slices through the wavelength domain will be shown as a plot of the delay against the absorption change. (Will only be shown if wavelengths are provided.)

<img src="/images/example plots/ex_waveslice.png" width="30%"/>

- *Heatmap*: The threedimensional data will be shown as a heatmap.

<img src="/images/example plots/ex_heatmap.png" width="30%"/>

- *All in One*: This plot shows the delay slices, wavelength slices and the heatmap next to eachother in a single image.

<img src="/images/example plots/ex_all.png" width="30%"/>

- *Concentrations (c/t)*: This plot displays the concentration development of each species by plotting the concentration against the delay.

<img src="/images/example plots/ex_concentrations.png" width="30%"/>

- *DAS/SAS(ΔA/λ)*: Depending on the evaluation method the decay associated spectra (for GLA) or the species associated spectra (for GTA) will be shown as plots of the absorption change against the wavelength.

<img src="/images/example plots/ex_DASSAS.png" width="30%"/>

- *Residuals*: Displays the residuals as a heatmap.

<img src="/images/example plots/ex_residuals.png" width="30%"/>

- *3D Contour*: Displays the data as an interactive 3D contour plot.

<img src="/images/example plots/ex_3D.png" width="30%"/>

**Plot Settings**

For some Plots other parameters need to be set.

- *Delay Slices*: Specific delays for the Delay Slices Plot.

- *Wavelength Slices*: Specific wavelengths for the Wavelength Slices Plot.

- *Contour Lines*: A value characterizing the number of lines shown in the heatmap, higher values show more lines. If not changed will be set to 20.

### Input Confirmation

After all plotting settings are done the program is ready to be executed. 

<img src="/images/GUI/Input Confirmation.png" width="50%"/>

On the Input Confirmation-tab all inputs given by the user will be displayed, so that they can be checked one last time. If everything is as it should be the program can be started by clicking the Confirm-Button.

### Results

The resulting plots and the evalutaion results and other fit statistics will be displayed in different popup windows after the evalutaions. In addition to that all plots and results will be saved in a new folder in the data directory called "evaluation". After closing the program the inputs will also be saved in the data directory and reloaded if the directory will be selected another time.

## Script

The general features of the GUI are also included in the script, although there are less settings regarding the plotting of single plots. However, this can be easily customized and will be explained at the end of this chapter.

### General settings

At the top of the script, the general settings will be found.

<img src="/images/script/settings.png" width="50%"/>

First, the `directory` to the folder containing the data needs to be provided. Files with the following names will be recognized:
> `/...lambda.txt` contains the wavelengths/nm,
> `/...delays.txt` contains the delays/ps,
> `/...spectra.txt` contains the absorption change.

Then the evaluation `model` can be selected. GLA will be used for `0`, for the GTA one of the eight preimplemented models `1`-`8` can be selected or `"custom"` for a custom matrix.

<img src="/images/script/models.png" width="50%"/>

The next settings are `w_bounds` and `d_bounds` which are the `[lower, upper]` bound for the `wavelengths` and `delays` where the original data will be cut off. If the data should not be cut the bounds can be set as 'None'.

The variables `orig`, `fit` and `resi` affect which plots of the original and fitted data will be plotted.

Options for `orig`:

- `0`: no plot will be generated

- `3`: this will show the *All-In-One*-plot of the original data

- `4`: this will show the *3D Contour*-plot of the original data

Options for `fit`:

- `0`: no plot will be generated

- `1`: the fitted values will be printed in the console and the results will be saved

- `2`: this will show the *All-In-One*-plot of the fitted data and the results will be saved

- `3`: with this option the values will be printed, the *All-In-One*-plot will be generated and the results will be saved

- `3`: with this option the values will be printed, the *3D Contour*-plot will be generated and the results will be saved

Options for `resi`:

- `0`: no plot will be generated

- `1`: the residuals will be plotted in a 1D plot of the residuals against the delays

- `2`: this will generate a heatmap of the residuals

- `3`: with this option both images will be shown

This option only works, if fit is not 0.

Lastly an optimizer algorithm needs to be set.

### Settings for the Decay Associated Spectra

In the next section if GLA (model = 0) was selected, `0`-`a` fixed and `0`-`b` variable values for the decay constants `tau`  need to be set. The fixed values won't be optimized, whereas the variable ones will be incuded in the fit. The total number of tau values `a`+`b` has to be at least `1`.

<img src="/images/script/gla.png" width="50%"/>

### Settings for the Species Associated Spectra

For each lifetime an upper and a lower bound can be set (`GTA_tau_lb`, `GTA_tau_ub`). They define the regions where the optimized lifetimes should be found. Should you not want to set a lower and/or upper limit for a certain lifetime, you can simply take `None` as an element of the list. If you wish not to set any bounds, write None instead of the list.

For the initial concentrations `C_0`, you will be asked to set `0` or `n` values with *n* corresponding to the number of species separated by commatas. If you leave the list empty, the concentration of species `1` will be set to `1` and the concentration of the other species to `0`.

Should you choose the model `"custom"` you can specify the matrix `M` at the end. It can be a list or an array either handwritten or imported from a file.

<img src="/images/script/gta.png" width="50%"/>

### Settings for the *all-in-one* plots

In the next section you can configure the settings for the *all-in-one* plots.

<img src="/images/script/plotting.png" width="50%"/>

You are offered the following possibilities:

- `wave`: the wavelengths shown in the (sub)plot *t/ΔA*

- `time`: the delays shown in the (sub)plot *ΔA/λ*

- `v_min` and `v_max`: the lower and upper boundaries for the colorbar in the heatmap, `None` for automatic determination.

- `cont`: a value characterizing the number of contour lines shown in the heatmap (sub)plot, higher values show more lines

- `mul`: the value by which the absorption data must be multiplied to get ΔA·10³

### Further customizing

The script can be used to better customize the images that will be generated.

If you want to create custom plots you can write the code below the calculation. Keep in mind that you still have to choose the right values for `model`, `d_limits`, `l_limits` and `C_0` in the settings at the beginning.

The methdod you will want to use to generate custom images is `Controller.plotCustom(wave, time, v_min, v_max, model, cont, custom, add, mul)`. Most of the variables have already been explained above.

*custom*: custom describes which subplots will be plotted

- `"1"`: chosen wavelength values will be plotted in a plot of the delays against the absorption change

- `"2"`: the absorption change will be plotted as a heatmap of the delays against the wavelenghts

- `"3"`: chosen delay values will be plotted in a plot of the absorption change against the wavelenghts

- `"1+2"`, `"1+3"`, `"2+3"`, `"1+2+3"`: this is an image of the two or three plots mentioned above combined

The title of the plot corresponds to the name of the image. Be careful not to overwrite images and instead use `add` to give your plots different titles.

Another plot can be plotted with `Controller.plotConcentrations(model)`. It shows the concentration of each species against the delays.

Furthermore the DAS or SAS can be plotted with `Controller.plotDAS(model, tau_fit)`. It is a plot of the absorption change against the wavelengths.

The images for both of the plots are presented in the section of the GUI.