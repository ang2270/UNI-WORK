-- for FilePath literals

module Watch
where

import Control.Concurrent (threadDelay)
import Control.Monad (forever)
import System.FSNotify

watch :: Action -> FilePath -> IO a
watch action targetDir =
    withManager $ \mgr -> do
        -- start a watching job (in the background)
        watchDir
            mgr -- manager
            targetDir -- directory to watch
            (const True) -- predicate
            action -- action

        -- sleep forever (until interrupted)
        forever $ threadDelay 1000000
