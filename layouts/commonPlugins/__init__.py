from .. import registry

registry.add("AreaDetector Common Plugins", path=__path__,
	qt_stylesheet = "layout.yml",
	css_stylesheet = "layout.yml",
	required_inputs=[
("PLUGINS", 
"""List of plugin data dictionaries:
	
  Instance: Plugin instance name
  Displays: UI Displays to link to
  Args: Arguments to pass to the displays
""")], 
example=
"""PLUGINS:
    - Instance: image1
      Displays: NDStdArrays.ui
      Args: "P=$(P),R=image1:"
        
#    - Instance: image2
#      Displays: NDStdArrays.ui
#      Args: "P=$(P),R=image2:"
        
    - Instance: Pva1
      Displays: NDPva.ui
      Args: "P=$(P),R=Pva1:"
            
#    - Instance: Proc1
#      Displays: NDProcess.ui
#      Args: "P=$(P),R=Proc1:"
            
    - Instance: Trans1
      Displays: NDTransform.ui
      Args: "P=$(P),R=Trans1"
            
    - Instance: CC1
      Displays: NDColorConvert.ui
      Args: "P=$(P),R=CC1:"
    
    - Instance: CC2
      Displays: NDColorConvert.ui
      Args: "P=$(P),R=CC2:"
        
    - Instance: Over1
      Displays: NDOverlay.ui
      Args: "P=$(P),R=Over1:"
            
    - Instance: ROI1
      Displays: NDROI.ui
      Args: "P=$(P),R=ROI1:"
    
    - Instance: ROI2
      Displays: NDROI.ui
      Args: "P=$(P),R=ROI2:"
        
    - Instance: ROI3
      Displays: NDROI.ui
      Args: "P=$(P),R=ROI3:"
        
    - Instance: ROI4
      Displays: NDROI.ui
      Args: "P=$(P),R=ROI4:"
                   
    - Instance: Stats1
      Displays: NDStats.ui
      Args: "P=$(P),R=Stats1:"
        
    - Instance: Stats2
      Displays: NDStats.ui
      Args: "P=$(P),R=Stats2:"
        
    - Instance: Stats3
      Displays: NDStats.ui
      Args: "P=$(P),R=Stats3:"
        
    - Instance: Stats4
      Displays: NDStats.ui
      Args: "P=$(P),R=Stats4:"
            
    - Instance: Stats5
      Displays: NDStats.ui
      Args: "P=$(P),R=Stats5:"
        
    - Instance: ROIStat1
      Displays: NDROIStat.ui
      Args: "P=$(P),R=ROIStat:"
            
    - Instance: CB1
      Displays: NDCircularBuff.ui
      Args: "P=$(P),R=CB1:"
            
    - Instance: FFT1
      Displays: NDFFT.ui
      Args: "P=$(P),R=FFT1:"
            
    - Instance: Codec1
      Displays: NDCodec.ui
      Args: "P=$(P),R=Codec1:"
        
    - Instance: Codec2
      Displays: NDCodec.ui
      Args: "P=$(P),R=Codec2:"
            
#    - Instance: BadPix1
#      Displays: NDBadPixel.ui
#      Args: "P=$(P),R=BadPix1:"
            
    - Instance: netCDF1
      Displays: NDFileNetCDF.ui
      Args: "P=$(P),R=netCDF1:"
            
    - Instance: TIFF1
      Displays: NDFileTIFF.ui
      Args: "P=$(P),R=TIFF1:"
            
    - Instance: JPEG1
      Displays: NDFileJPEG.ui
      Args: "P=$(P),R=JPEG1:"
        
    - Instance: Nexus1
      Displays: NDFileNexus.ui
      Args: "P=$(P),R=Nexus1:"
        
    - Instance: HDF1
      Displays: NDFileHDF5.ui
      Args: "P=$(P),R=HDF1:"
        
    - Instance: Scatter1
      Displays: NDScatter.ui
      Args: "P=$(P),R=Scatter1:"
        
    - Instance: Gather1
      Displays: NDGather.ui
      Args: "P=$(P),R=Gather1:"
""")
