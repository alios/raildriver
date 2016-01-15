{-# LANGUAGE CPP #-}

#if __GLASGOW_HASKELL__ >= 709
{-# LANGUAGE Safe #-}
#elif __GLASGOW_HASKELL__ >= 701
{-# LANGUAGE Trustworthy #-}
#endif
-----------------------------------------------------------------------------
-- |
-- Module      :  Win32.Raildriver
-- Copyright   :  (c) Markus Barenhoff, 2016
-- License     :  BSD-style (see the file LICENSE)
--
-- Maintainer  :  Markus Barenhoff <mbarenh@alios.org>
-- Stability   :  provisional
-- Portability :  portable
--
-- A collection of FFI declarations for interfacing with raildriver.dll.
--
-----------------------------------------------------------------------------

module Win32.Raildriver 
    ( setRailSimConnected
    , getLocoName
    ) where

import Win32.Raildriver.FFI
import Foreign.C.String


-- | Connect/Disconnect (based on the argument 'c') to the simulator.
--   Must be called with 'True' before any other API call from this library.
setRailSimConnected :: Bool -> IO ()
setRailSimConnected c = c_SetRailSimConnected c

getLocoName :: IO String
getLocoName = c_GetLocoName >>= peekCString