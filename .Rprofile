local_lib <- file.path(getwd(), ".r-lib")
if (!dir.exists(local_lib)) {
  dir.create(local_lib, recursive = TRUE, showWarnings = FALSE)
}
.libPaths(c(normalizePath(local_lib, winslash = "/", mustWork = FALSE), .libPaths()))
