
module Main(main) where

import Win32.Raildriver


main :: IO ()
main = 
  do print "raildriver-server"
     setRailSimConnected True
     ln <- getLocoName
     print $ "getLocoName: " ++ ln
     setRailSimConnected False
  