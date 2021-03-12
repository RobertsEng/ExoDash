### Exoplanet Dashboard

**Kevin Roberts**


The initial goal of this project is to make a web-deployable dashboard displaying key exoplanet-related information, including the approximate positions of systems containing **confirmed exoplanets** over an artist-rendering of the Milky Way, keeping in mind the practical limitations of such a mapping. The ultimate intention for this process involves the dashboard regularly (perhaps weekly or daily) importing data from the *NASA Exoplanet Archive* into a dataframe containing celestial coordinates for the host stars of confirmed exoplanets. In order to enable superimposition of exoplanets on a 2D galaxy map via the *MWPlot library*, the program will then use the SkyCoord package from astropy to convert equatorial coordinates for each system into galactocentric coordinates.

This project uses the mw_plot library by Henry Leung and the images contained therein (MW_bg_annotate.jpg and MW_bg_unannotate.jpg) by **NASA/JPL-Caltech/R. Hurt (SSC/Caltech)**.

Currently the project has several functions:

#### makegalaxymap()

This function creates a plot of the positions of stars confirmed to be hosts to exoplanets, and superimposes those positions on an artist rendering of the Milky Way.

    def makegalaxymap():
      # Sets the service to be used for querying.
      service = vo.dal.TAPService('https://exoplanetarchive.ipac.caltech.edu/TAP')

      # Queries the Planetary Composite Parameters table of the Exoplanet Archive for the host name, RA, DEC, and distance of exoplanets' host stars.
      resultset = service.search('SELECT hostname, ra, dec, sy_dist FROM pscomppars')

      # Converts the votable to an astropy table.    
      planetarycompositetable = resultset.to_table()

      # Converts the astropy table to a Pandas dataframe.   
      planetarycomposite = planetarycompositetable.to_pandas()

      # Drops rows containing NaN values from the dataframe
      planetarycompositeclean = planetarycomposite.dropna() 

      # I reset the index to ensure that deletion of NaN rows doesn't introduce indexing issues later.
      planetarycompositeclean.reset_index(inplace = True) 

      # Drops duplicate host star names, keeping the first instance of each duplicate found.  
      planetarycompositeclean = planetarycompositeclean.drop_duplicates(subset ='hostname', keep = 'first')

      # I reset the index to ensure that deletion of NaN rows doesn't introduce indexing issues later.
      planetarycompositeclean.reset_index(inplace = True)

      # Creates a SkyCoord object containing coordinate information for each exoplanet host.
      starskycoord = SkyCoord(ra = planetarycompositeclean['ra']*u.deg, dec = planetarycompositeclean['dec']*u.deg, distance = planetarycompositeclean['sy_dist']*u.pc, frame = 'icrs')

      # Formats the coordinates into the galactocentric format.
      stargalactocentric = starskycoord.galactocentric

      # Creates and renders the exoplanet host galaxy plot and saves a local copy of the figure.
      plot_instance = MWPlot(mode='face-on', center=(0,0)*u.kpc, radius = 90750*u.lyr, unit  = u.kpc, coord='galactocentric', annotation= False, rot90=2, grayscale=False)
      plot_instance.title = 'Exoplanets Across the Galaxy'  
      plot_instance.fontsize = 35 
      plot_instance.figsize = (20, 20) 
      plot_instance.dpi = 200  
      plot_instance.cmap = 'viridis'  
      plot_instance.clim = (0, 10) 
      plot_instance.imalpha = 0.85  
      plot_instance.s = 5  
      plot_instance.tight_layout = True # whether plt.tight_layout() will be run
      plot_instance.mw_scatter(-stargalactocentric.x, stargalactocentric.y,'fuchsia')
      plot_instance.mw_scatter(x = 8.3*u.kpc, y = 0*u.kpc, c = 'lime')
      plot_instance.savefig('exoplanets.png')
      plot_instance.show()

![image](https://user-images.githubusercontent.com/48961863/110524589-34fa2780-80d9-11eb-8192-cdefef8659cb.png)

#### numplanetsbydate()

This function produces a plot of the number of detected exoplanets across time.

    def numplanetsbydate():
      # Sets the service to be used for querying.
      service = vo.dal.TAPService('https://exoplanetarchive.ipac.caltech.edu/TAP')

      # Queries the Planetary Composite Parameters table at NASA's Exoplanet Archive for exoplanet name and year of discovery
      planetdatequery = service.search('SELECT pl_name, disc_year FROM pscomppars')

      # Converts the votable to an astropy table object
      planetdatetable = planetdatequery.to_table()

      # Converts the astropy table object to a Pandas dataframe
      planetdate = planetdatetable.to_pandas()

      # Drops NaN values from the dataframe
      planetdate = planetdate.dropna()

      # Produce a count of the number of exoplanets per year of discovery
      planetdategrouped = planetdate.groupby(by = 'disc_year').count()

      # Resets the index of the dataframe
      planetdategrouped.reset_index(inplace = True)

      # Renames the columns of the dataframe for readability
      planetdategrouped.rename(columns = {'pl_name':'Number of Exoplanets', 'disc_year':'Discovery Year'}, inplace = True)

      # Produces a plot of the number of detected exoplanets per year of discovery
      plt.figure(figsize = (15,10))
      planetdateplot = sns.barplot(data = planetdategrouped, x = 'Discovery Year', y = 'Number of Exoplanets')
      plt.show()
      
![image](https://user-images.githubusercontent.com/48961863/110525229-f6b13800-80d9-11eb-9314-43cd0cc02303.png)

#### cumuplanets()

This function produces a plot of the *cumulative* number of detected exoplanets across time.
 
    def cumuplanets():
      # Sets the service to be used for querying.
      service = vo.dal.TAPService('https://exoplanetarchive.ipac.caltech.edu/TAP')

      # Queries the Planetary Composite Parameters table at NASA's Exoplanet Archive for exoplanet name and year of discovery
      planetdatequery = service.search('SELECT pl_name, disc_year FROM pscomppars')

      # Converts the votable to an astropy table object
      planetdatetable = planetdatequery.to_table()

      # Converts the astropy table object to a Pandas dataframe
      planetdate = planetdatetable.to_pandas()

      # Drops NaN values from the dataframe
      planetdate = planetdate.dropna()

      # Produces a count of the number of exoplanets per year of discovery
      planetdategrouped = planetdate.groupby(by = 'disc_year').count()

      # Resets the index of the dataframe
      planetdategrouped.reset_index(inplace = True)

      # Renames the columns of the dataframe for readability
      planetdategrouped.rename(columns = {'pl_name':'Number of Exoplanets', 'disc_year':'Discovery Year'}, inplace = True)

      # Produces a new column with a cumulative sum of exoplanets per year
      planetdategrouped['Cumulative Number of Exoplanets'] = planetdategrouped['Number of Exoplanets'].cumsum()

      # Produces a plot of the cumulative number of detected exoplanets across year of discovery
      plt.figure(figsize = (15,10))
      planetdateplot = sns.barplot(data = planetdategrouped, x = 'Discovery Year', y = 'Cumulative Number of Exoplanets')
      plt.show()
      
![image](https://user-images.githubusercontent.com/48961863/110525262-00d33680-80da-11eb-861a-96eeb769460b.png)

#### numplanetsbydateandmethod()

This function produces a bar plot of the number of exoplanets detected per year of discovery, stacked by method of discovery.

    def numplanetsbydateandmethod():
    
      # Sets the service to be used for querying.
      service = vo.dal.TAPService('https://exoplanetarchive.ipac.caltech.edu/TAP')

      # Queries the Planetary Composite Parameters table at NASA's Exoplanet Archive for exoplanet name, discovery method used, and year of discovery
      planetdatequery = service.search('SELECT pl_name, discoverymethod, disc_year FROM pscomppars')

      # Converts votable to an astropy Table object
      planetdatetable = planetdatequery.to_table()

      # Converts astropy table object o a pandas dataframe
      planetdate = planetdatetable.to_pandas()

      # Drops NaN values from the dataframe 
      planetdate = planetdate.dropna()

      # Creates a count of exoplanets grouped by year of discovery and method of discovery.

      planetdategrouped = planetdate.groupby(by = ['disc_year', 'discoverymethod']).count()

      # Resets the index of the dataframe.
      planetdategrouped.reset_index(inplace = True)

      # Renames columns for readabiltiy 
      planetdategrouped.rename(columns = {'pl_name':'Number of Exoplanets', 'disc_year':'Discovery Year', 'discoverymethod':'Discovery Method'}, inplace = True)

      # Replaces all discovery method strings with clean strings (didn't have much luck applying TRIM method in SQL to clean this up within the SELECT statement)
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].astype(str)
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Disk Kinematics'", 'Disk Kinematics')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Eclipse Timing Variations'", 'Eclipse Timing Variations')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Imaging'", 'Imaging')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Microlensing'", 'Microlensing')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Orbital Brightness Modulation'", 'Orbital Brightness Modulation')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Pulsar Timing'", 'Pulsar Timing')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Pulsation Timing Variations'", 'Pulsation Timing Variations')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Radial Velocity'", 'Radial Velocity')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Transit'", 'Transit')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Transit Timing Variations'", 'Transit Timing Variations')
      planetdategrouped['Discovery Method'] = planetdategrouped['Discovery Method'].str.replace("b'Astrometry'", 'Astrometry')

      # Reshapes dataframe into a pivot table
      planetdatepivot = planetdategrouped.pivot(index = 'Discovery Year', columns = 'Discovery Method', values = 'Number of Exoplanets')

      # Creates a bar plot of the number of exoplanets detected per year of discovery, stacked by method of discovery
      plot = planetdatepivot.plot.bar(stacked = True, figsize = (15, 10), cmap = 'Set3', width = 0.6)
      plot.set_ylabel('Number of Exoplanets')
      plot.set_xlabel('Discovery Year')
      plot.grid(False)
   
![image](https://user-images.githubusercontent.com/48961863/110525292-0af53500-80da-11eb-96f4-342964fb2cc7.png)
