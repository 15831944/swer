project(OpenCamLib)

cmake_minimum_required(VERSION 2.4)



# some options to set what is built:
option(BUILD_CXX_LIB
  "Build/install the pure c++ libocl library? " OFF)

option(BUILD_PY_LIB 
  "Build/install the python ocl library? " ON)

option(BUILD_CUTSIM
  "Build/install the ocl cutting simulation (requires OpenGL and Qt) ? " OFF)

option(BUILD_DOC
  "Build/install the ocl documentation? " OFF)

if (NOT BUILD_CXX_LIB)
    MESSAGE(STATUS " Note: will NOT build pure c++ library")
endif(NOT BUILD_CXX_LIB)

if (NOT BUILD_PY_LIB)
    MESSAGE(STATUS " Note: will NOT build python library")
endif(NOT BUILD_PY_LIB)

if (NOT BUILD_CUTSIM)
    MESSAGE(STATUS " Note: will NOT build ocl cutting simulation")
endif(NOT BUILD_CUTSIM)

if (NOT BUILD_DOC)
    MESSAGE(STATUS " Note: will NOT build ocl documentation")
endif(NOT BUILD_DOC)


#
# Turn compiler warnings up to 11, at least with gcc.  I dont know how to
# do this with other compilers we might support and I'm leaving it up to
# the relevant platform maintainers...
# #include'ing the boost graph-library creates deprecated warnings
# thus we use now use -Wno-deprecated here.
#
if (CMAKE_BUILD_TOOL MATCHES "make")
    MESSAGE(STATUS "setting gcc options: -Wall -Werror -Wno-deprecated -pedantic-errors")
    add_definitions(-Wall  -Wno-deprecated )
    # qt does not like this: -Werror -pedantic-errors
endif (CMAKE_BUILD_TOOL MATCHES "make")

# find out the number of CPUs
# from: http://www.kitware.com/blog/home/post/63
if(NOT DEFINED PROCESSOR_COUNT)
  # Unknown:
  set(PROCESSOR_COUNT 0)
  # Linux:
  set(cpuinfo_file "/proc/cpuinfo")
  if(EXISTS "${cpuinfo_file}")
    file(STRINGS "${cpuinfo_file}" procs REGEX "^processor.: [0-9]+$")
    list(LENGTH procs PROCESSOR_COUNT)
  endif()
  MESSAGE(STATUS "Number of processors on this system " ${PROCESSOR_COUNT} )
  # FIXME: how do we have cmake/make use all the processors?
endif()


#
# this figures out the Python include directories and adds them to the
# header file search path
#
execute_process(
    COMMAND python-config --includes
    COMMAND sed -r "s/-I//g; s/ +/;/g"
    COMMAND tr -d '\n'
    OUTPUT_VARIABLE Python_Includes
)
include_directories(${Python_Includes})

# run get_revision.py which generates revision.h needed by ocl.revision()
MESSAGE(STATUS "running get_revision.py to generate revision.h")
execute_process(
     # we pass the SRC directory as a parameter to the python script
     COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/get_revision.py ${CMAKE_CURRENT_SOURCE_DIR}
)

include_directories(${CMAKE_CURRENT_BINARY_DIR})


# find BOOST and boost-python
find_package( Boost COMPONENTS python REQUIRED)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
    MESSAGE(STATUS "found Boost: " ${Boost_LIB_VERSION})
    MESSAGE(STATUS "boost-incude dirs are: " ${Boost_INCLUDE_DIRS})
    MESSAGE(STATUS "boost-python lib is: " ${Boost_PYTHON_LIBRARY})
    MESSAGE(STATUS "boost_LIBRARY_DIRS is: " ${Boost_LIBRARY_DIRS})
    MESSAGE(STATUS "Boost_LIBRARIES is: " ${Boost_LIBRARIES})    
endif()

#
# find OpenMP
#

find_package( OpenMP REQUIRED )

IF (OPENMP_FOUND)
    MESSAGE(STATUS "found OpenMP, compiling with flags: " ${OpenMP_CXX_FLAGS} )

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
ENDIF(OPENMP_FOUND)

#
# for cutsim, find OpenGL and Qt.
#

if (BUILD_CUTSIM)
    MESSAGE(STATUS "Cutting simulation requires OpenGL and Qt...")
    find_package(OpenGL REQUIRED)
    if(OPENGL_FOUND)
        MESSAGE(STATUS "found OPENGL, lib = " ${OPENGL_LIBRARIES} )
    endif(OPENGL_FOUND)
    
    FIND_PACKAGE(Qt4 COMPONENTS QtCore QtGui QtXml QtOpenGL REQUIRED)
    message(STATUS " qmake = ${QT_QMAKE_EXECUTABLE}") 
    INCLUDE(${QT_USE_FILE})
    MESSAGE(STATUS "QT_USE_FILE = " ${QT_USE_FILE} )
    
    set (MOC_HEADERS  # these headers need Qt MOCing
        ${OpenCamLib_SOURCE_DIR}/cutsim/glwidget.h
    )
    
    
endif(BUILD_CUTSIM)

# this defines the source-files

set(OCL_GEO_SRC
    ${OpenCamLib_SOURCE_DIR}/geo/arc.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/bbox.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/ccpoint.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/clpoint.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/line.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/path.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/point.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/stlreader.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/stlsurf.cpp
    ${OpenCamLib_SOURCE_DIR}/geo/triangle.cpp
)

set(OCL_CUTTER_SRC
    ${OpenCamLib_SOURCE_DIR}/cutters/ballcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/bullcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/compositecutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/conecutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/millingcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/cylcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/ellipse.cpp
    ${OpenCamLib_SOURCE_DIR}/cutters/ellipseposition.cpp
)

set(OCL_DROPCUTTER_SRC
    ${OpenCamLib_SOURCE_DIR}/dropcutter/batchdropcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/dropcutter/pointdropcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/dropcutter/pathdropcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/dropcutter/adaptivepathdropcutter.cpp
)

set(OCL_ALGO_SRC
    
    
    ${OpenCamLib_SOURCE_DIR}/algo/batchpushcutter.cpp
    ${OpenCamLib_SOURCE_DIR}/algo/fiberpushcutter.cpp
    
   

    ${OpenCamLib_SOURCE_DIR}/algo/interval.cpp
    ${OpenCamLib_SOURCE_DIR}/algo/fiber.cpp
    ${OpenCamLib_SOURCE_DIR}/algo/waterline.cpp
    ${OpenCamLib_SOURCE_DIR}/algo/adaptivewaterline.cpp

    ${OpenCamLib_SOURCE_DIR}/algo/weave2.cpp
    
    

)

set(OCL_VORONOI_SRC
    ${OpenCamLib_SOURCE_DIR}/voronoi/voronoidiagram.cpp
    ${OpenCamLib_SOURCE_DIR}/voronoi/voronoidiagram_checker.cpp
    ${OpenCamLib_SOURCE_DIR}/voronoi/facegrid.cpp
)
set(OCL_COMMON_SRC
    ${OpenCamLib_SOURCE_DIR}/common/numeric.cpp
    ${OpenCamLib_SOURCE_DIR}/common/lineclfilter.cpp
)

set( OCL_CUTSIM_SRC
    ${OpenCamLib_SOURCE_DIR}/cutsim/volume.cpp
    ${OpenCamLib_SOURCE_DIR}/cutsim/octnode.cpp
    ${OpenCamLib_SOURCE_DIR}/cutsim/octree.cpp
    ${OpenCamLib_SOURCE_DIR}/cutsim/marching_cubes.cpp
    ${OpenCamLib_SOURCE_DIR}/cutsim/glwidget.cpp 
    ${OpenCamLib_SOURCE_DIR}/cutsim/gldata.cpp 
        
)

set( OCL_INCLUDE_FILES
    ${CMAKE_CURRENT_BINARY_DIR}/revision.h
    
    ${OpenCamLib_SOURCE_DIR}/geo/arc.h
    ${OpenCamLib_SOURCE_DIR}/geo/bbox.h
    ${OpenCamLib_SOURCE_DIR}/geo/ccpoint.h
    ${OpenCamLib_SOURCE_DIR}/geo/clpoint.h
    ${OpenCamLib_SOURCE_DIR}/geo/line.h
    ${OpenCamLib_SOURCE_DIR}/geo/path.h
    ${OpenCamLib_SOURCE_DIR}/geo/stlreader.h
    ${OpenCamLib_SOURCE_DIR}/geo/stlsurf.h
    ${OpenCamLib_SOURCE_DIR}/geo/triangle.h
    ${OpenCamLib_SOURCE_DIR}/geo/point.h
    
    ${OpenCamLib_SOURCE_DIR}/cutters/ballcutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/bullcutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/compositecutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/conecutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/cylcutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/ellipseposition.h
    ${OpenCamLib_SOURCE_DIR}/cutters/millingcutter.h
    ${OpenCamLib_SOURCE_DIR}/cutters/ellipse.h
    
    ${OpenCamLib_SOURCE_DIR}/dropcutter/adaptivepathdropcutter.h
    ${OpenCamLib_SOURCE_DIR}/dropcutter/pathdropcutter.h
    ${OpenCamLib_SOURCE_DIR}/dropcutter/batchdropcutter.h
    ${OpenCamLib_SOURCE_DIR}/dropcutter/pointdropcutter.h
    
    
    
    ${OpenCamLib_SOURCE_DIR}/common/brent_zero.h
    ${OpenCamLib_SOURCE_DIR}/common/kdnode.h
    ${OpenCamLib_SOURCE_DIR}/common/kdtree.h
    ${OpenCamLib_SOURCE_DIR}/common/numeric.h
    ${OpenCamLib_SOURCE_DIR}/common/lineclfilter.h
    ${OpenCamLib_SOURCE_DIR}/common/clfilter.h
    ${OpenCamLib_SOURCE_DIR}/common/halfedgediagram.hpp
    
    ${OpenCamLib_SOURCE_DIR}/algo/operation.h
    ${OpenCamLib_SOURCE_DIR}/algo/batchpushcutter.h
    ${OpenCamLib_SOURCE_DIR}/algo/fiberpushcutter.h
    ${OpenCamLib_SOURCE_DIR}/algo/fiber.h
    ${OpenCamLib_SOURCE_DIR}/algo/interval.h
    ${OpenCamLib_SOURCE_DIR}/algo/waterline.h
    ${OpenCamLib_SOURCE_DIR}/algo/adaptivewaterline.h
    ${OpenCamLib_SOURCE_DIR}/algo/weave2.h
    ${OpenCamLib_SOURCE_DIR}/algo/weave2_typedef.h
    
    ${OpenCamLib_SOURCE_DIR}/voronoi/voronoidiagram_graph.hpp
    ${OpenCamLib_SOURCE_DIR}/voronoi/voronoidiagram.hpp
    ${OpenCamLib_SOURCE_DIR}/voronoi/voronoidiagram_checker.hpp
    ${OpenCamLib_SOURCE_DIR}/voronoi/facegrid.hpp

    
    
    ${OpenCamLib_SOURCE_DIR}/algo/tsp.h
)

set( OCL_CUTSIM_INCLUDE_FILES
    ${OpenCamLib_SOURCE_DIR}/cutsim/octnode.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/octree.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/volume.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/marching_cubes.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/gldata.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/glwidget.h
    ${OpenCamLib_SOURCE_DIR}/cutsim/p3.h
)

# this branches into the dirs and compiles stuff there
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/cutters  )
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/geo  )
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/algo  ) 
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/voronoi  ) 
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/dropcutter  ) 
ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/common  ) 
# ADD_SUBDIRECTORY( ${OpenCamLib_SOURCE_DIR}/cutsim  )

# include dirs
include_directories( ${OpenCamLib_SOURCE_DIR}/cutters )
include_directories( ${OpenCamLib_SOURCE_DIR}/geo )
include_directories( ${OpenCamLib_SOURCE_DIR}/algo )
include_directories( ${OpenCamLib_SOURCE_DIR}/voronoi )
include_directories( ${OpenCamLib_SOURCE_DIR}/dropcutter )
include_directories( ${OpenCamLib_SOURCE_DIR}/common )
# include_directories( ${OpenCamLib_SOURCE_DIR}/cutsim )
include_directories( ${OpenCamLib_SOURCE_DIR} )

if (BUILD_PY_LIB)
    # this makes the ocl Python module
    add_library(
        ocl 
        MODULE
        ocl_cutters.cpp
        ocl_geometry.cpp
        #ocl_cutsim.cpp
        ocl_algo.cpp
        ocl_dropcutter.cpp
        ocl_voronoi.cpp
        ocl.cpp
    )

    MESSAGE(STATUS "linking python binary ocl.so with boost: " ${Boost_PYTHON_LIBRARY})
    target_link_libraries(ocl ocl_common ocl_dropcutter ocl_cutters ocl_voronoi ocl_geo ocl_algo ${Boost_LIBRARIES} ) #${Boost_PYTHON_LIBRARY})
    # 
    # this makes the lib name ocl.so and not libocl.so
    set_target_properties(ocl PROPERTIES PREFIX "") 

endif (BUILD_PY_LIB)




# this is the C++ shared library
if (BUILD_CXX_LIB)
    add_library(
        libocl
        SHARED
        ${OCL_GEO_SRC}
        ${OCL_CUTTER_SRC}
        ${OCL_VORONOI_SRC}
        ${OCL_ALGO_SRC}
        ${OCL_DROPCUTTER_SRC}
        ${OCL_COMMON_SRC}
    )
    # target_link_libraries(libocl ocl_algo)
    set_target_properties(libocl PROPERTIES PREFIX "") 
endif (BUILD_CXX_LIB)

# this is the cutting sim
if(BUILD_CUTSIM)
    qt4_wrap_cpp(MOC_OUTFILES ${MOC_HEADERS})
    add_library(cutsim SHARED 
        # ${OpenCamLib_SOURCE_DIR}/cutsim/glwidget.cpp 
        # ${OpenCamLib_SOURCE_DIR}/cutsim/gldata.cpp 
        ${OCL_CUTSIM_SRC}
        
        ${MOC_OUTFILES}
    )
    target_link_libraries(cutsim  ${OPENGL_LIBRARIES})
endif(BUILD_CUTSIM)

#
# this figures out where to install the Python modules
#

execute_process(
    COMMAND python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
    OUTPUT_VARIABLE Python_site_packages
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
MESSAGE(STATUS "Python libraries will be installed to: " ${Python_site_packages})

if (BUILD_PY_LIB)
    # this installs the python library
    install(
        TARGETS ocl
        LIBRARY DESTINATION ${Python_site_packages}
    )


    # these are the python helper lib-files such as camvtk.py 
    install(
        DIRECTORY ../lib/
        DESTINATION ${Python_site_packages}
        PATTERN .svn EXCLUDE
    )
endif (BUILD_PY_LIB)

# this installs the c++ library
if (BUILD_CXX_LIB)
    install(
        TARGETS libocl
        LIBRARY 
        DESTINATION lib/opencamlib
        ARCHIVE DESTINATION lib/opencamlib
        PERMISSIONS OWNER_READ OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    )

    # this installs the c++ include headers
    install(
        FILES ${OCL_INCLUDE_FILES}
        DESTINATION include/opencamlib
        PERMISSIONS OWNER_READ GROUP_READ WORLD_READ
    )
endif (BUILD_CXX_LIB)

# install cutsim
if(BUILD_CUTSIM)
    install(
        TARGETS cutsim
        LIBRARY 
        DESTINATION lib/opencamlib
        ARCHIVE DESTINATION lib/opencamlib
        PERMISSIONS OWNER_READ OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    )
    # this installs the c++ include headers
    install(
        FILES ${OCL_CUTSIM_INCLUDE_FILES}
        DESTINATION include/opencamlib
        PERMISSIONS OWNER_READ GROUP_READ WORLD_READ
    )
endif (BUILD_CUTSIM)

#
# this installs the examples
#

# install(
#     DIRECTORY ../scripts/
#    DESTINATION share/doc/python-opencam/examples
#    PATTERN .svn EXCLUDE
# )

# the example STL files
# install(
#     DIRECTORY ../stl/
#     DESTINATION share/doc/python-opencam/examples/stl
#     PATTERN .svn EXCLUDE
# )


#
# build & install documentation (if Doxygen is available)
#

if (BUILD_DOC)

FIND_PACKAGE(Doxygen)
IF (DOXYGEN_FOUND)
    MESSAGE(STATUS "Found doxygen. ")
    
    # this works around a bug in cmake 2.4 (Ubuntu Hardy)
    execute_process(
        COMMAND mkdir -p doc/html doc/latex
    )

    FIND_PACKAGE(LATEX)
    IF    (NOT LATEX_COMPILER)
        MESSAGE(STATUS "latex command LATEX_COMPILER not found but usually required. You will probably get warnings and user inetraction on doxy run.")
    ENDIF (NOT LATEX_COMPILER)
    IF    (NOT MAKEINDEX_COMPILER)
        MESSAGE(STATUS "makeindex command MAKEINDEX_COMPILER not found but usually required.")
    ENDIF (NOT MAKEINDEX_COMPILER)
    IF    (NOT DVIPS_CONVERTER)
        MESSAGE(STATUS "dvips command DVIPS_CONVERTER not found but usually required.")
    ENDIF (NOT DVIPS_CONVERTER)
    
    if (EXISTS Doxyfile)
        set(DOXY_CONFIG Doxyfile)
    endif (EXISTS Doxyfile)

    add_custom_command(
        OUTPUT
            doc/latex/index.tex
            doc/html/index.html
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXY_CONFIG}
        COMMENT building LaTex & HTML docs
    )

    add_custom_target(
        doc
        DEPENDS doc/latex/index.tex
    )


    IF (EXISTS ${PDFLATEX_COMPILER})
        add_custom_command(
            OUTPUT doc/latex/refman.pdf
            DEPENDS doc/latex/index.tex
            WORKING_DIRECTORY doc/latex
            COMMAND make pdf
            COMMENT building PDF docs
            COMMAND mv refman.pdf ../ocl-manual.pdf
        )

        add_custom_target(
            doc-pdf
            DEPENDS doc/latex/refman.pdf
        )

        add_dependencies(doc doc-pdf)
    ELSE (EXISTS ${PDFLATEX_COMPILER}) 
       message(STATUS "pdflatex compiler not found, PDF docs will not be built")
   ENDIF (EXISTS ${PDFLATEX_COMPILER})


    add_custom_target(
        doc-latex
        DEPENDS doc/latex/index.tex
    )

    #install(
    #    DIRECTORY doc/latex/
    #    DESTINATION share/doc/python-opencam/pdf
    #    FILES_MATCHING PATTERN *.pdf
    #)

    #install(
    #    FILES doc/ocl-manual.pdf
    #    DESTINATION share/doc/python-opencam/pdf
    #)

    #install(
    #    DIRECTORY doc/html
    #    DESTINATION share/doc/python-opencam/
    #)

ENDIF(DOXYGEN_FOUND)
endif (BUILD_DOC)


# "make package" stuff
set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "opencamlib@googlegroups.com")
set(CPACK_PACKAGE_NAME "opencamlib")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "opencamlib")
set(CPACK_DEBIAN_PACKAGE_SECTION "science")
set(CPACK_DEBIAN_PACKAGE_VERSION "")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "python, libboost-python-dev, libgomp1" )
SET(CPACK_PACKAGE_VERSION_MAJOR "11")
SET(CPACK_PACKAGE_VERSION_MINOR "06")
SET(CPACK_PACKAGE_VERSION_PATCH "0")
include(CPack)
