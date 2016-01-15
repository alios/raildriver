{-# LANGUAGE ForeignFunctionInterface #-}

-----------------------------------------------------------------------------
-- |
-- Module      :  Win32.Raildriver.FFI
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

module Win32.Raildriver.FFI
    (c_SetRailSimConnected
    ) where

import Foreign
import Foreign.C.Types

c_SetRailSimConnected :: Bool -> IO ()
c_SetRailSimConnected c = undefined

