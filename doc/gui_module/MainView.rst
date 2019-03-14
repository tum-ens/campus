MainView.py Module
******************


The MainView module is our application frame or main window. It consists of 3 major views:

1. Overview Tab. This is the GeneralView module.
2. Transmission Tab. This is the TransmissionView module.
3. A tab for modeling the energy system for each site. This is the RESView module.
 
=======
Methods
=======

1. *__init__(self, controller):*

 The function does the following activities:

 - Build File menu and bind each menu item to a method within the view
 - Create main panel
 - Create a notebook to hold the tabs
 - Create first tab as GeneralView instance, and it to the notebook as “Overview”
 - Create second tab as TrasmissionView instance, and add it to the notebook as “Transmssion”
 - Put the notebook in as Sizer and set the panel content to that sizer.
 
2. *AddRESTab(self, controller, siteName):*

 This function is called when the user add a new site to the system. It does the following:

 - Create a new tab for that site (a RESView instance)
 - Add this tab to notebook

3. *RemoveRESTab(self, sites):*

 This function is called when the user remove a site or more from the system. It does the following:

 - For each site of the removed sites

  - Loop on the notebook tabs (pages), from index 2. As index 0 is for the Overview tab, and index 1 is for Transmission tab.

   - Remove the RESView tab (page) from the note book, if its associated name is equal to the site that the user want to remove

 - Set the Overview tab as the selected tab

4. *GetTrnsmTab(self):*

 This function returns the RESView of the transmission tab. Page #1 in the notebook.

5. *OnPageSelected(self, event):*

 This function is triggered when the user change the selected tab in the notebook.

 - First, we get the tab index
 - If the index is 0 (Overview tab) or 1 (Transmission tab), then nothing to do
 - Get the RESView instance of the selected tab
 - Refresh the view to redraw itself
 - Send a notification that the active RES tab is now for Site X. The controller is actually interested in such notification, so it can obtain a reference for the model of the current active site. So, when the user add/remove process for instance, the controller will be able to update the model of that particular site.

6. *OnOpen(self, event):*

 This function is triggered when the user select “Load Config” from the file menu.

 - It creates an open file dialog and set the filter to json files.
 - If the user selected a file, the method will send a notification to load the configuration. The controller subscribe on such notification and it will start the loading process.

7. *OnSave(self, event):*

 This function is triggered when the user select “Save Config” from the file menu.

 - It creates a save file dialog and set the filter to json files.

  - It warns the user if he tried to override existing file (wx.FD_OVERWRITE_PROMPT)

 - If the user selected a file, the method will send a notification to save the system. The controller subscribe on such notification and it will start the saving process of the whole modeled system.

8. *OnQuit(self, event):*

 This function is triggered when the user select “Exit” from the file menu. It simply terminate the program.
