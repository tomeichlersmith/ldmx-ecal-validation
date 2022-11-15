"""Hold the two or more files we are comparing together in one class"""

import uproot
import matplotlib.pyplot as plt
import os

class FileEntry :
    """File entry in Differ object

    This should not be used directly by the user
    """

    def __init__(self, *args) :
        self.__file = uproot.open(args[0])
        self.__name = args[1]
        if len(args) > 2 :
            self.__colmod = args[2]
        else :
            self.__colmod = None
        self.__df = None

    def keys(self, *args, **kwargs) :
        """Callback into uproot keys

        Helpful for exploring the file when trying to decide
        what to plot within a notebook
        """
        return self.__file.keys(*args, **kwargs)
    
    def events(self, **kwargs) :
        """Callback for retrieving a full in-memory data frame of the events
        
        All key-word arguments are passed to the uproot.arrays method.
        
        We change the default 'library' to be pandas which can be overridden
        by a user if desired.
        """

        if 'library' not in kwargs :
            kwargs['library'] = 'pd'
        return self.__file['LDMX_Events'].arrays(**kwargs)
    
    def load(self, manipulation = None, **kwargs) :
        """Instead of giving the events data frame to the caller,
        we store the dataframe here for later batch processing
        
        manipulation is a function operating on the loaded dataframe
        which is there for people to rename columns, calculate new
        columns, etc...
        
        All the kwargs are simply provided to events for selecting
        the branches of LDMX_Events to load into memory.
        """
        self.__df = self.events(**kwargs)
        if manipulation is not None :
            manipulation(self.__df)
    
    def manipulate(self, manipulation) :
        """Apply the passed manipulation to the dataframe"""
        manipulation(self.__df)
    
    def plot1d(self, ax, obj_name, **hist_kwargs) :
        """Plot the input uproot object as a histogram on the input axes

        If obj_name is not a str, we assume that it is a callable and will
        provide the in-memory dataframe. An exception is thrown if the dataframe
        has not been loaded.
        
        If the dataframe of events has been loaded and the obj_name is a
        member of that dataframe, we use that dataframe to fill the histogram.
        
        If the uproot_obj is already a histogram we import its values and use
        them directly. If the uproot_obj is a TBranch, then we pull its values
        into memory and fill the histogram.

        The input 'obj_name' is transformed by __colmod if that member is set.
        """
        
        if 'histtype' not in hist_kwargs :
            hist_kwargs['histtype'] = 'step'
        if 'linewidth' not in hist_kwargs :
            hist_kwargs['linewidth'] = 2
        if 'label' not in hist_kwargs :
            hist_kwargs['label'] = self.__name
            
        if not isinstance(obj_name, str) :
                if self.__df is None :
                        raise KeyError('Cannot use dynamic value calculations without loading the dataframe.')
                return ax.hist(obj_name(self.__df), **hist_kwargs)

        if self.__df is not None and obj_name in self.__df :
                return ax.hist(self.__df[obj_name], **hist_kwargs)
        
        if self.__colmod is not None :
            obj_name = self.__colmod(obj_name)

        obj = self.__file[obj_name]

        if issubclass(type(obj), uproot.behaviors.TH1.Histogram) :
            edges = obj.axis('x').edges()
            dim = len(edges.shape)
            if dim > 1 :
                raise KeyError(f'Attempted to do a 1D plot of a {dim} dimension histogram.')
            return ax.hist((edges[1:]+edges[:-1])/2, bins=edges, weights=obj.values(), **hist_kwargs)
        else :
            return ax.hist(obj.array(library='pd').values, **hist_kwargs)        

class Differ :
    """Differ allowing easy comparison of "similar" files

    The basic requirement of all files passed is that the columns
    of data in the 'LDMX_Events' TTree are named exactly the same.
    This is an easy requirement if the files are generated using
    the same configuration script and/or the same installation of
    ldmx-sw.

    Parameters
    ----------
    grp_name : str
        Name to include in legend title to differentiate
        this group of plots from another
    args : list of 2-tuples
        Each entry is a 2-tuple (file_path, name) where file_path
        specifies the file to open and name is what should appear
        in plot legends
    kwargs : dict
        These keyword arguments are passed to plt.figure for creationg
        of the figure we draw on.

    Example
    -------
    Opening a differ is pretty quick and lightweight.
    We do open the files with `uproot` and access the event tree.

        d = Differ('v3.2.0-alpha',('path/to/v12.root','v12'),('path/to/v14.root','v14'))

    Without any other options, the plotting with show the plot as if
    we are in an interactive notebook.

        d.plot1d('EcalSimHits_valid/EcalSimHits_valid.edep_')
    """

    def __init__(self, grp_name, *args) :
        self.grp_name = grp_name
        self.files = [ FileEntry(*pack) for pack in args ]

    def plot1d(self, column, xlabel, 
              ylabel = 'Count',
              yscale = 'log',
              ylim = (None,None),
              out_dir = None, file_name = None,
              **hist_kwargs) :
        fig = plt.figure('differ',figsize=(11,8))
        ax = fig.subplots()

        for f in self.files :
            f.plot1d(ax, column, **hist_kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_yscale(yscale)
        ax.set_ylim(*ylim)
        ax.legend(title=self.grp_name)

        if out_dir is None :
            plt.show()
        else :
            fn = column
            if file_name is not None :
                fn = file_name
            fig.savefig(os.path.join(out_dir,fn)+'.pdf', bbox_inches='tight')
            fig.clf()

    def load(self, **kwargs) :
        """Load all of the event data frames into memory
        
        The key-word arguments are used in each FileEntry's events call
        to specify which branches (if not all of them) should be loaded
        into memory and what manipulation (if any) to do.
        """
        for f in self.files :
            f.load(**kwargs)
            
    def manipulate(self, manipulation) :
        for f in self.files :
            f.manipulate(manipulation)