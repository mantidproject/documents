/* Automatically generated file. Do not edit.
* Format:     ANSI C source code
* Creator:    McStas <http://www.mcstas.org>
* Instrument: /home/mcstas/test.instr (My_Instrument)
* Date:       Wed Nov  9 09:52:27 2016
* File:       /home/mcstas/test.c
* Compile:    cc -o My_Instrument.out /home/mcstas/test.c
* CFLAGS=
*/


#define MCCODE_STRING "McStas 2.3 - Apr. 06, 2016"
#define FLAVOR "mcstas"
#define FLAVOR_UPPER "MCSTAS"
#define MC_USE_DEFAULT_MAIN
#define MC_TRACE_ENABLED
#define MC_EMBEDDED_RUNTIME

#line 1 "mccode-r.h"
/*******************************************************************************
*
* McCode, neutron/xray ray-tracing package
*         Copyright (C) 1997-2009, All rights reserved
*         Risoe National Laboratory, Roskilde, Denmark
*         Institut Laue Langevin, Grenoble, France
*
* Runtime: share/mccode-r.h
*
* %Identification
* Written by: KN
* Date:    Aug 29, 1997
* Release: McStas 2.3
* Version: $Revision$
*
* Runtime system header for McStas/McXtrace.
*
* In order to use this library as an external library, the following variables
* and macros must be declared (see details in the code)
*
*   struct mcinputtable_struct mcinputtable[];
*   int mcnumipar;
*   char mcinstrument_name[], mcinstrument_source[];
*   int mctraceenabled, mcdefaultmain;
*   extern MCNUM  mccomp_storein[];
*   extern MCNUM  mcAbsorbProp[];
*   extern MCNUM  mcScattered;
*   #define MCCODE_STRING "the McStas/McXtrace version"
*
* Usage: Automatically embbeded in the c code.
*
* $Id$
*
*******************************************************************************/

#ifndef MCCODE_R_H
#define MCCODE_R_H "$Revision$"

#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <limits.h>
#include <errno.h>
#include <time.h>
#include <float.h>
#include <inttypes.h>

/* If the runtime is embedded in the simulation program, some definitions can
be made static. */

#ifdef MC_EMBEDDED_RUNTIME
#define mcstatic static
#else
#define mcstatic
#endif

#ifdef __dest_os
#if (__dest_os == __mac_os)
#define MAC
#endif
#endif

#ifdef __FreeBSD__
#define NEED_STAT_H
#endif

#if defined(__APPLE__) && defined(__GNUC__)
#define NEED_STAT_H
#endif

#ifdef NEED_STAT_H
#include <sys/stat.h>
#endif

#ifndef MC_PATHSEP_C
#ifdef WIN32
#define MC_PATHSEP_C '\\'
#define MC_PATHSEP_S "\\"
#else  /* !WIN32 */
#define MC_PATHSEP_C '/'
#define MC_PATHSEP_S "/"
#endif /* !WIN32 */
#endif /* MC_PATHSEP_C */



/* the version string is replaced when building distribution with mkdist */
#ifndef MCCODE_STRING
#define MCCODE_STRING "McStas 2.3 - Apr. 06, 2016"
#endif

#ifndef MCCODE_DATE
#define MCCODE_DATE "Apr. 06, 2016"
#endif

#ifndef MCCODE_VERSION
#define MCCODE_VERSION "2.3"
#endif

#ifndef MCCODE_NAME
#define MCCODE_NAME "McStas"
#endif

#ifndef MCCODE_PARTICLE
#define MCCODE_PARTICLE "neutron"
#endif

#ifndef MCCODE_LIBENV
#define MCCODE_LIBENV "MCSTAS"
#endif

#ifndef FLAVOR_UPPER
#define FLAVOR_UPPER MCCODE_NAME
#endif

#ifdef MC_PORTABLE
#ifndef NOSIGNALS
#define NOSIGNALS 1
#endif
#endif

#ifdef MAC
#ifndef NOSIGNALS
#define NOSIGNALS 1
#endif
#endif

#if (USE_MPI == 0)
#undef USE_MPI
#endif

#ifdef USE_MPI  /* default is to disable signals with MPI, as MPICH uses them to communicate */
#ifndef NOSIGNALS
#define NOSIGNALS 1
#endif
#endif

#if (NOSIGNALS == 0)
#undef NOSIGNALS
#endif

/* Note: the enum instr_formal_types definition MUST be kept
synchronized with the one in mccode.h and with the
instr_formal_type_names array in cogen.c. */
enum instr_formal_types
{
	instr_type_double, instr_type_int, instr_type_string
};
struct mcinputtable_struct { /* defines instrument parameters */
	char *name; /* name of parameter */
	void *par;  /* pointer to instrument parameter (variable) */
	enum instr_formal_types type;
	char *val;  /* default value */
};

typedef double MCNUM;
typedef struct { MCNUM x, y, z; } Coords;
typedef MCNUM Rotation[3][3];

/* the following variables are defined in the McStas generated C code
but should be defined externally in case of independent library usage */
#ifndef DANSE
extern struct mcinputtable_struct mcinputtable[]; /* list of instrument parameters */
extern int    mcnumipar;                          /* number of instrument parameters */
extern char   mcinstrument_name[], mcinstrument_source[]; /* instrument name and filename */
extern char  *mcinstrument_exe;                           /* executable path = argv[0] or NULL */
extern MCNUM  mccomp_storein[]; /* 11 coords * number of components in instrument */
extern MCNUM  mcAbsorbProp[];
extern MCNUM  mcScattered;      /* number of SCATTER calls in current component */
extern MCNUM  mcRestore;        /* Flag to indicate if neutron needs to be restored */
#ifndef MC_ANCIENT_COMPATIBILITY
extern int mctraceenabled, mcdefaultmain;
#endif
#endif


/* Useful macros ============================================================ */

/* MPI stuff */

#ifdef USE_MPI
#include "mpi.h"

#ifdef OMPI_MPI_H  /* openmpi does not use signals: we may install our sighandler */
#undef NOSIGNALS
#endif

/*
* MPI_MASTER(i):
* execution of i only on master node
*/
#define MPI_MASTER(statement) { \
  if(mpi_node_rank == mpi_node_root)\
  { statement; } \
}

#ifndef MPI_REDUCE_BLOCKSIZE
#define MPI_REDUCE_BLOCKSIZE 1000
#endif

int mc_MPI_Sum(double* buf, long count);
int mc_MPI_Send(void *sbuf, long count, MPI_Datatype dtype, int dest);
int mc_MPI_Recv(void *rbuf, long count, MPI_Datatype dtype, int source);

/* MPI_Finalize exits gracefully and should be preferred to MPI_Abort */
#define exit(code) do {                                   \
    MPI_Finalize();                                       \
    exit(code);                                           \
  } while(0)

#else /* !USE_MPI */
#define MPI_MASTER(instr) instr
#endif /* USE_MPI */

#ifdef USE_MPI
static int mpi_node_count;
#endif

#ifdef USE_THREADS  /* user want threads */
#error Threading (USE_THREADS) support has been removed for very poor efficiency. Use MPI/SSH grid instead.
#endif


void   mcset_ncount(unsigned long long count);    /* wrapper to get mcncount */
unsigned long long int mcget_ncount(void);            /* wrapper to set mcncount */
unsigned long long mcget_run_num(void);           /* wrapper to get mcrun_num=0:mcncount */


												  /* Following part is only embedded when not redundant with mccode.h ========= */

#ifndef MCCODE_H

#ifndef NOSIGNALS
#include <signal.h>
#define SIG_MESSAGE(msg) strcpy(mcsig_message, msg);
#else
#define SIG_MESSAGE(msg)
#endif /* !NOSIGNALS */

												  /* Useful macros and constants ============================================== */

#ifndef FLT_MAX
#define FLT_MAX         3.40282347E+38F /* max decimal value of a "float" */
#endif

#ifndef MIN
#define MIN(a, b)  (((a) < (b)) ? (a) : (b))
#endif
#ifndef MAX
#define MAX(a, b)  (((a) > (b)) ? (a) : (b))
#endif
#ifndef SQR
#define SQR(x) ( (x) * (x) )
#endif
#ifndef SIGN
#define SIGN(x) (((x)>0.0)?(1):(-1))
#endif

#ifndef PI
# ifdef M_PI
#  define PI M_PI
# else
#  define PI 3.14159265358979323846
# endif
#endif

#define RAD2MIN  ((180*60)/PI)
#define MIN2RAD  (PI/(180*60))
#define DEG2RAD  (PI/180)
#define RAD2DEG  (180/PI)
#define FWHM2RMS 0.424660900144    /* Convert between full-width-half-max and */
#define RMS2FWHM 2.35482004503     /* root-mean-square (standard deviation) */
#define HBAR     1.05457168e-34    /* [Js] h bar Planck constant CODATA 2002 */
#define MNEUTRON 1.67492728e-27    /* [kg] mass of neutron CODATA 2002 */
#define GRAVITY  9.81              /* [m/s^2] gravitational acceleration */
#define NA       6.02214179e23     /* [#atoms/g .mole] Avogadro's number*/


												  /* wrapper to get absolute and relative position of comp */
												  /* mccomp_posa and mccomp_posr are defined in McStas generated C code */
#define POS_A_COMP_INDEX(index) \
    (mccomp_posa[index])
#define POS_R_COMP_INDEX(index) \
    (mccomp_posr[index])
												  /* number of SCATTER calls in current comp: mcScattered defined in generated C code */
#define SCATTERED mcScattered
												  /* Flag to indicate if neutron needs to be restored: mcRestore defined in generated C code */
#define RESTORE mcRestore


												  /* Retrieve component information from the kernel */
												  /* Name, position and orientation (both absolute and relative)  */
												  /* Any component: For "redundancy", see comment by KN */
#define tmp_name_comp(comp) #comp
#define NAME_COMP(comp) tmp_name_comp(comp)
#define tmp_pos_a_comp(comp) (mcposa ## comp)
#define POS_A_COMP(comp) tmp_pos_a_comp(comp)
#define tmp_pos_r_comp(comp) (mcposr ## comp)
#define POS_R_COMP(comp) tmp_pos_r_comp(comp)
#define tmp_rot_a_comp(comp) (mcrota ## comp)
#define ROT_A_COMP(comp) tmp_rot_a_comp(comp)
#define tmp_rot_r_comp(comp) (mcrotr ## comp)
#define ROT_R_COMP(comp) tmp_rot_r_comp(comp)

												  /* Current component name, index, position and orientation */
#define NAME_CURRENT_COMP  NAME_COMP(mccompcurname)
#define INDEX_CURRENT_COMP mccompcurindex
#define POS_A_CURRENT_COMP POS_A_COMP(mccompcurname)
#define POS_R_CURRENT_COMP POS_R_COMP(mccompcurname)
#define ROT_A_CURRENT_COMP ROT_A_COMP(mccompcurname)
#define ROT_R_CURRENT_COMP ROT_R_COMP(mccompcurname)

												  /* Note: The two-stage approach to MC_GETPAR is NOT redundant; without it,
												  * after #define C sample, MC_GETPAR(C,x) would refer to component C, not to
												  * component sample. Such are the joys of ANSI C.

												  * Anyway the usage of MCGETPAR requires that we use sometimes bare names...
												  */
#define MC_GETPAR2(comp, par) (mcc ## comp ## _ ## par)
#define MC_GETPAR(comp, par) MC_GETPAR2(comp,par)

												  /* MCDISPLAY/trace and debugging message sent to stdout */
#ifdef MC_TRACE_ENABLED
#define DEBUG
#endif

#ifdef DEBUG
#define mcDEBUG_INSTR() if(!mcdotrace); else { printf("INSTRUMENT:\n"); printf("Instrument '%s' (%s)\n", mcinstrument_name, mcinstrument_source); }
#define mcDEBUG_COMPONENT(name,c,t) if(!mcdotrace); else {\
  printf("COMPONENT: \"%s\"\n" \
         "POS: %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n", \
         name, c.x, c.y, c.z, t[0][0], t[0][1], t[0][2], \
         t[1][0], t[1][1], t[1][2], t[2][0], t[2][1], t[2][2]); \
  printf("Component %30s AT (%g,%g,%g)\n", name, c.x, c.y, c.z); \
  }
#define mcDEBUG_INSTR_END() if(!mcdotrace); else printf("INSTRUMENT END:\n");
#define mcDEBUG_ENTER() if(!mcdotrace); else printf("ENTER:\n");
#define mcDEBUG_COMP(c) if(!mcdotrace); else printf("COMP: \"%s\"\n", c);
#define mcDEBUG_LEAVE() if(!mcdotrace); else printf("LEAVE:\n");
#define mcDEBUG_ABSORB() if(!mcdotrace); else printf("ABSORB:\n");
#else
#define mcDEBUG_INSTR()
#define mcDEBUG_COMPONENT(name,c,t)
#define mcDEBUG_INSTR_END()
#define mcDEBUG_ENTER()
#define mcDEBUG_COMP(c)
#define mcDEBUG_LEAVE()
#define mcDEBUG_ABSORB()
#endif

												  // mcDEBUG_STATE and mcDEBUG_SCATTER are defined by mcstas-r.h and mcxtrace-r.h



#ifdef TEST
#define test_printf printf
#else
#define test_printf while(0) printf
#endif

												  /* send MCDISPLAY message to stdout to show gemoetry */
void mcdis_magnify(char *what);
void mcdis_line(double x1, double y1, double z1,
	double x2, double y2, double z2);
void mcdis_dashed_linemcdis_dashed_line(double x1, double y1, double z1,
	double x2, double y2, double z2, int n);
void mcdis_multiline(int count, ...);
void mcdis_rectangle(char* plane, double x, double y, double z,
	double width, double height);
void mcdis_box(double x, double y, double z,
	double width, double height, double length);
void mcdis_circle(char *plane, double x, double y, double z, double r);

/* selection of random number generator. default is MT */
#ifndef MC_RAND_ALG
#define MC_RAND_ALG 1
#endif

#if MC_RAND_ALG == 0
/* Use system random() (not recommended). */
#  define MC_RAND_MAX RAND_MAX
#elif MC_RAND_ALG == 1
/* "Mersenne Twister", by Makoto Matsumoto and Takuji Nishimura. */
#  define MC_RAND_MAX ((unsigned long)0xffffffff)
#  define random mt_random
#  define srandom mt_srandom
#elif MC_RAND_ALG == 2
/* Algorithm used in McStas CVS-080208 and earlier (not recommended). */
#  define MC_RAND_MAX 0x7fffffff
#  define random mc_random
#  define srandom mc_srandom
#else
#  error "Bad value for random number generator choice."
#endif

typedef int mc_int32_t;
mc_int32_t mc_random(void);
void mc_srandom(unsigned int x);
unsigned long mt_random(void);
void mt_srandom(unsigned long x);

double rand01();
double randpm1();
double rand0max(double max);
double randminmax(double min, double max);

double randnorm(void);
double randtriangle(void);

#ifndef DANSE
void mcinit(void);
void mcraytrace(void);
void mcsave(FILE *);
void mcfinally(void);
void mcdisplay(void);
#endif

/* simple vector algebra ==================================================== */
#define vec_prod(x, y, z, x1, y1, z1, x2, y2, z2) \
	vec_prod_func(&x, &y, &z, x1, y1, z1, x2, y2, z2)
mcstatic inline void vec_prod_func(double *x, double *y, double *z,
	double x1, double y1, double z1, double x2, double y2, double z2);

mcstatic inline double scalar_prod(
	double x1, double y1, double z1, double x2, double y2, double z2);

#define NORM(x,y,z) \
	norm_func(&x, &y, &z)
mcstatic inline void norm_func(double *x, double *y, double *z) {
	double temp = (*x * *x) + (*y * *y) + (*z * *z);
	if (temp != 0) {
		temp = sqrt(temp);
		*x /= temp;
		*y /= temp;
		*z /= temp;
	}
}
#define normal_vec(nx, ny, nz, x, y, z) \
    normal_vec_func(&(nx), &(ny), &(nz), x, y, z)
mcstatic inline void normal_vec_func(double *nx, double *ny, double *nz,
	double x, double y, double z);

/**
* Rotate the vector vx,vy,vz psi radians around the vector ax,ay,az
* and put the result in x,y,z.
*/
#define rotate(x, y, z, vx, vy, vz, phi, ax, ay, az) \
  do { \
    double mcrt_tmpx = (ax), mcrt_tmpy = (ay), mcrt_tmpz = (az); \
    double mcrt_vp, mcrt_vpx, mcrt_vpy, mcrt_vpz; \
    double mcrt_vnx, mcrt_vny, mcrt_vnz, mcrt_vn1x, mcrt_vn1y, mcrt_vn1z; \
    double mcrt_bx, mcrt_by, mcrt_bz; \
    double mcrt_cos, mcrt_sin; \
    NORM(mcrt_tmpx, mcrt_tmpy, mcrt_tmpz); \
    mcrt_vp = scalar_prod((vx), (vy), (vz), mcrt_tmpx, mcrt_tmpy, mcrt_tmpz); \
    mcrt_vpx = mcrt_vp*mcrt_tmpx; \
    mcrt_vpy = mcrt_vp*mcrt_tmpy; \
    mcrt_vpz = mcrt_vp*mcrt_tmpz; \
    mcrt_vnx = (vx) - mcrt_vpx; \
    mcrt_vny = (vy) - mcrt_vpy; \
    mcrt_vnz = (vz) - mcrt_vpz; \
    vec_prod(mcrt_bx, mcrt_by, mcrt_bz, \
             mcrt_tmpx, mcrt_tmpy, mcrt_tmpz, mcrt_vnx, mcrt_vny, mcrt_vnz); \
    mcrt_cos = cos((phi)); mcrt_sin = sin((phi)); \
    mcrt_vn1x = mcrt_vnx*mcrt_cos + mcrt_bx*mcrt_sin; \
    mcrt_vn1y = mcrt_vny*mcrt_cos + mcrt_by*mcrt_sin; \
    mcrt_vn1z = mcrt_vnz*mcrt_cos + mcrt_bz*mcrt_sin; \
    (x) = mcrt_vpx + mcrt_vn1x; \
    (y) = mcrt_vpy + mcrt_vn1y; \
    (z) = mcrt_vpz + mcrt_vn1z; \
  } while(0)

/**
* Mirror (xyz) in the plane given by the point (rx,ry,rz) and normal (nx,ny,nz)
*
* TODO: This define is seemingly never used...
*/
#define mirror(x,y,z,rx,ry,rz,nx,ny,nz) \
  do { \
    double mcrt_tmpx= (nx), mcrt_tmpy = (ny), mcrt_tmpz = (nz); \
    double mcrt_tmpt; \
    NORM(mcrt_tmpx, mcrt_tmpy, mcrt_tmpz); \
    mcrt_tmpt=scalar_prod((rx),(ry),(rz),mcrt_tmpx,mcrt_tmpy,mcrt_tmpz); \
    (x) = rx -2 * mcrt_tmpt*mcrt_rmpx; \
    (y) = ry -2 * mcrt_tmpt*mcrt_rmpy; \
    (z) = rz -2 * mcrt_tmpt*mcrt_rmpz; \
  } while (0)

Coords coords_set(MCNUM x, MCNUM y, MCNUM z);
Coords coords_get(Coords a, MCNUM *x, MCNUM *y, MCNUM *z);
Coords coords_add(Coords a, Coords b);
Coords coords_sub(Coords a, Coords b);
Coords coords_neg(Coords a);
Coords coords_scale(Coords b, double scale);
double coords_sp(Coords a, Coords b);
Coords coords_xp(Coords b, Coords c);
void   coords_print(Coords a);
mcstatic inline void coords_norm(Coords* c);

void rot_set_rotation(Rotation t, double phx, double phy, double phz);
int  rot_test_identity(Rotation t);
void rot_mul(Rotation t1, Rotation t2, Rotation t3);
void rot_copy(Rotation dest, Rotation src);
void rot_transpose(Rotation src, Rotation dst);
Coords rot_apply(Rotation t, Coords a);

void mccoordschange(Coords a, Rotation t, double *x, double *y, double *z,
	double *vx, double *vy, double *vz, double *sx, double *sy, double *sz);
void
mccoordschange_polarisation(Rotation t, double *sx, double *sy, double *sz);

double mcestimate_error(double N, double p1, double p2);
void mcreadparams(void);

/* this is now in mcstas-r.h and mcxtrace-r.h as the number of state parameters is no longer equal*/
/* void mcsetstate(double x, double y, double z, double vx, double vy, double vz,
double t, double sx, double sy, double sz, double p);
*/
void mcgenstate(void);

/* trajectory/shape intersection routines */
int inside_rectangle(double, double, double, double);
int box_intersect(double *dt_in, double *dt_out, double x, double y, double z,
	double vx, double vy, double vz, double dx, double dy, double dz);
int cylinder_intersect(double *t0, double *t1, double x, double y, double z,
	double vx, double vy, double vz, double r, double h);
int sphere_intersect(double *t0, double *t1, double x, double y, double z,
	double vx, double vy, double vz, double r);
/* second order equation roots */
int solve_2nd_order(double *t1, double *t2,
	double A, double B, double C);

/* random vector generation to shape */
void randvec_target_circle(double *xo, double *yo, double *zo,
	double *solid_angle, double xi, double yi, double zi, double radius);
#define randvec_target_sphere randvec_target_circle
void randvec_target_rect_angular(double *xo, double *yo, double *zo,
	double *solid_angle,
	double xi, double yi, double zi, double height, double width, Rotation A);
#define randvec_target_rect(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9)  randvec_target_rect_real(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,0,0,0,1)
void randvec_target_rect_real(double *xo, double *yo, double *zo,
	double *solid_angle,
	double xi, double yi, double zi, double height, double width, Rotation A,
	double lx, double ly, double lz, int order);

/* this is the main() */
int mccode_main(int argc, char *argv[]);


#endif /* !MCCODE_H */

#ifndef MCCODE_R_IO_H
#define MCCODE_R_IO_H "$Revision$"

#if (USE_NEXUS == 0)
#undef USE_NEXUS
#endif

#ifndef CHAR_BUF_LENGTH
#define CHAR_BUF_LENGTH 1024
#endif

/* I/O section part ========================================================= */

/* ========================================================================== */

/*                               MCCODE_R_IO_C                                */

/* ========================================================================== */


/* main DETECTOR structure which stores most information to write to data files */
struct mcdetector_struct {
	char   filename[CHAR_BUF_LENGTH];   /* file name of monitor */
	char   position[CHAR_BUF_LENGTH];   /* position of detector component */
	char   component[CHAR_BUF_LENGTH];  /* component instance name */
	char   instrument[CHAR_BUF_LENGTH]; /* instrument name */
	char   type[CHAR_BUF_LENGTH];       /* data type, e.g. 0d, 1d, 2d, 3d */
	char   user[CHAR_BUF_LENGTH];       /* user name, e.g. HOME */
	char   date[CHAR_BUF_LENGTH];       /* date of simulation end/write time */
	char   title[CHAR_BUF_LENGTH];      /* title of detector */
	char   xlabel[CHAR_BUF_LENGTH];     /* X axis label */
	char   ylabel[CHAR_BUF_LENGTH];     /* Y axis label */
	char   zlabel[CHAR_BUF_LENGTH];     /* Z axis label */
	char   xvar[CHAR_BUF_LENGTH];       /* X variable name */
	char   yvar[CHAR_BUF_LENGTH];       /* Y variable name */
	char   zvar[CHAR_BUF_LENGTH];       /* Z variable name */
	char   ncount[CHAR_BUF_LENGTH];     /* number of events initially generated */
	char   limits[CHAR_BUF_LENGTH];     /* X Y Z limits, e.g. [xmin xmax ymin ymax zmin zmax] */
	char   variables[CHAR_BUF_LENGTH];  /* variables written into data block */
	char   statistics[CHAR_BUF_LENGTH]; /* center, mean and half width along axis */
	char   signal[CHAR_BUF_LENGTH];     /* min max and mean of signal (data block) */
	char   values[CHAR_BUF_LENGTH];     /* integrated values e.g. [I I_err N] */
	double xmin, xmax;                   /* min max of axes */
	double ymin, ymax;
	double zmin, zmax;
	double intensity;                   /* integrated values for data block */
	double error;
	double events;
	double min;                         /* statistics for data block */
	double max;
	double mean;
	double centerX;                     /* statistics for axes */
	double halfwidthX;
	double centerY;
	double halfwidthY;
	int    rank;                        /* dimensionaly of monitor, e.g. 0 1 2 3 */
	char   istransposed;                /* flag to transpose matrix for some formats */

	long   m, n, p;                       /* dimensions of data block and along axes */
	long   date_l;                      /* same as date, but in sec since 1970 */

	double *p0, *p1, *p2;               /* pointers to saved data, NULL when freed */
	char   format[CHAR_BUF_LENGTH];    /* format for file generation */
};

typedef struct mcdetector_struct MCDETECTOR;

static   char *mcdirname = NULL;      /* name of output directory */
static   char *mcsiminfo_name = "mccode";  /* default output sim file name */
char    *mcformat = NULL;      /* NULL (default) or a specific format */

							   /* file I/O definitions and function prototypes */

#ifndef MC_EMBEDDED_RUNTIME /* the mcstatic variables (from mccode-r.c) */
extern FILE * mcsiminfo_file;     /* handle to the output siminfo file */
extern int    mcgravitation;      /* flag to enable gravitation */
extern int    mcdotrace;          /* flag to print MCDISPLAY messages */
#else
mcstatic FILE *mcsiminfo_file = NULL;
#endif

/* I/O function prototypes ================================================== */

/* output functions */
MCDETECTOR mcdetector_out_0D(char *t, double p0, double p1, double p2, char *c, Coords pos);
MCDETECTOR mcdetector_out_1D(char *t, char *xl, char *yl,
	char *xvar, double x1, double x2, long n,
	double *p0, double *p1, double *p2, char *f, char *c, Coords pos);
MCDETECTOR mcdetector_out_2D(char *t, char *xl, char *yl,
	double x1, double x2, double y1, double y2, long m,
	long n, double *p0, double *p1, double *p2, char *f,
	char *c, Coords pos);
MCDETECTOR mcdetector_out_list(char *t, char *xl, char *yl,
	long m, long n,
	double *p1, char *f,
	char *c, Coords posa);

/* wrappers to output functions, that automatically set NAME and POSITION */
#define DETECTOR_OUT(p0,p1,p2) mcdetector_out_0D(NAME_CURRENT_COMP,p0,p1,p2,NAME_CURRENT_COMP,POS_A_CURRENT_COMP)
#define DETECTOR_OUT_0D(t,p0,p1,p2) mcdetector_out_0D(t,p0,p1,p2,NAME_CURRENT_COMP,POS_A_CURRENT_COMP)
#define DETECTOR_OUT_1D(t,xl,yl,xvar,x1,x2,n,p0,p1,p2,f) \
     mcdetector_out_1D(t,xl,yl,xvar,x1,x2,n,p0,p1,p2,f,NAME_CURRENT_COMP,POS_A_CURRENT_COMP)
#define DETECTOR_OUT_2D(t,xl,yl,x1,x2,y1,y2,m,n,p0,p1,p2,f) \
     mcdetector_out_2D(t,xl,yl,x1,x2,y1,y2,m,n,p0,p1,p2,f,NAME_CURRENT_COMP,POS_A_CURRENT_COMP)

#ifdef USE_NEXUS
#include "napi.h"
NXhandle nxhandle;
#endif

#endif /* ndef MCCODE_R_IO_H */

#endif /* MCCODE_R_H */
/* End of file "mccode-r.h". */

#line 688 "/home/mcstas/test.c"

#line 1 "mcstas-r.h"
/*******************************************************************************
*
* McStas, neutron ray-tracing package
*         Copyright (C) 1997-2009, All rights reserved
*         Risoe National Laboratory, Roskilde, Denmark
*         Institut Laue Langevin, Grenoble, France
*
* Runtime: share/mcstas-r.h
*
* %Identification
* Written by: KN
* Date:    Aug 29, 1997
* Release: McStas X.Y
* Version: $Revision$
*
* Runtime system header for McStas.
*
* In order to use this library as an external library, the following variables
* and macros must be declared (see details in the code)
*
*   struct mcinputtable_struct mcinputtable[];
*   int mcnumipar;
*   char mcinstrument_name[], mcinstrument_source[];
*   int mctraceenabled, mcdefaultmain;
*   extern MCNUM  mccomp_storein[];
*   extern MCNUM  mcAbsorbProp[];
*   extern MCNUM  mcScattered;
*   #define MCCODE_STRING "the McStas version"
*
* Usage: Automatically embbeded in the c code.
*
* $Id$
*
*******************************************************************************/

#ifndef MCSTAS_R_H
#define MCSTAS_R_H "$Revision$"

/* Following part is only embedded when not redundent with mcstas.h ========= */

#ifndef MCCODE_H

#define AA2MS    629.622368        /* Convert k[1/AA] to v[m/s] */
#define MS2AA    1.58825361e-3     /* Convert v[m/s] to k[1/AA] */
#define K2V      AA2MS
#define V2K      MS2AA
#define Q2V      AA2MS
#define V2Q      MS2AA
#define SE2V     437.393377        /* Convert sqrt(E)[meV] to v[m/s] */
#define VS2E     5.22703725e-6     /* Convert (v[m/s])**2 to E[meV] */

#define SCATTER do {mcDEBUG_SCATTER(mcnlx, mcnly, mcnlz, mcnlvx, mcnlvy, mcnlvz, \
        mcnlt,mcnlsx,mcnlsy,mcnlsz, mcnlp); mcScattered++;} while(0)
#define ABSORB do {mcDEBUG_STATE(mcnlx, mcnly, mcnlz, mcnlvx, mcnlvy, mcnlvz, \
        mcnlt,mcnlsx,mcnlsy,mcnlsz, mcnlp); mcDEBUG_ABSORB(); MAGNET_OFF; goto mcabsorb;} while(0)

#define STORE_NEUTRON(index, x, y, z, vx, vy, vz, t, sx, sy, sz, p) \
  mcstore_neutron(mccomp_storein,index, x, y, z, vx, vy, vz, t, sx, sy, sz, p);
#define RESTORE_NEUTRON(index, x, y, z, vx, vy, vz, t, sx, sy, sz, p) \
  mcrestore_neutron(mccomp_storein,index, &x, &y, &z, &vx, &vy, &vz, &t, &sx, &sy, &sz, &p);

#define MAGNET_ON \
  do { \
    mcMagnet = 1; \
  } while(0)

#define MAGNET_OFF \
  do { \
    mcMagnet = 0; \
  } while(0)

#define ALLOW_BACKPROP \
  do { \
    mcallowbackprop = 1; \
  } while(0)

#define DISALLOW_BACKPROP \
  do { \
    mcallowbackprop = 0; \
  } while(0)

#define PROP_MAGNET(dt) \
  do { \
  }while (0)
/* change coordinates from local system to magnet system */
/*    Rotation rotLM, rotTemp; \
Coords   posLM = coords_sub(POS_A_CURRENT_COMP, mcMagnetPos); \
rot_transpose(ROT_A_CURRENT_COMP, rotTemp); \
rot_mul(rotTemp, mcMagnetRot, rotLM); \
mcMagnetPrecession(mcnlx, mcnly, mcnlz, mcnlt, mcnlvx, mcnlvy, mcnlvz, \
&mcnlsx, &mcnlsy, &mcnlsz, dt, posLM, rotLM); \
} while(0)
*/

#define mcPROP_DT(dt) \
  do { \
    if (mcMagnet && dt > 0) PROP_MAGNET(dt);\
    mcnlx += mcnlvx*(dt); \
    mcnly += mcnlvy*(dt); \
    mcnlz += mcnlvz*(dt); \
    mcnlt += (dt); \
    if (isnan(p) || isinf(p)) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }\
  } while(0)

/* ADD: E. Farhi, Aug 6th, 2001 PROP_GRAV_DT propagation with acceleration */
#define PROP_GRAV_DT(dt, Ax, Ay, Az) \
  do { \
    if(dt < 0 && mcallowbackprop == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }\
    if (mcMagnet) printf("Spin precession gravity\n"); \
    mcnlx  += mcnlvx*(dt) + (Ax)*(dt)*(dt)/2; \
    mcnly  += mcnlvy*(dt) + (Ay)*(dt)*(dt)/2; \
    mcnlz  += mcnlvz*(dt) + (Az)*(dt)*(dt)/2; \
    mcnlvx += (Ax)*(dt); \
    mcnlvy += (Ay)*(dt); \
    mcnlvz += (Az)*(dt); \
    mcnlt  += (dt); \
    DISALLOW_BACKPROP;\
  } while(0)


#define PROP_DT(dt) \
  do { \
    if(dt < 0) { RESTORE=1; goto mcabsorbComp; }; \
    if (mcgravitation) { Coords mcLocG; double mc_gx, mc_gy, mc_gz; \
    mcLocG = rot_apply(ROT_A_CURRENT_COMP, coords_set(0,-GRAVITY,0)); \
    coords_get(mcLocG, &mc_gx, &mc_gy, &mc_gz); \
    PROP_GRAV_DT(dt, mc_gx, mc_gy, mc_gz); } \
    else mcPROP_DT(dt); \
    DISALLOW_BACKPROP;\
  } while(0)


#define PROP_Z0 \
  do { \
    if (mcgravitation) { Coords mcLocG; int mc_ret; \
    double mc_dt, mc_gx, mc_gy, mc_gz; \
    mcLocG = rot_apply(ROT_A_CURRENT_COMP, coords_set(0,-GRAVITY,0)); \
    coords_get(mcLocG, &mc_gx, &mc_gy, &mc_gz); \
    mc_ret = solve_2nd_order(&mc_dt, NULL, -mc_gz/2, -mcnlvz, -mcnlz); \
    if (mc_ret && mc_dt>=0) {PROP_GRAV_DT(mc_dt, mc_gx, mc_gy, mc_gz); mcnlz=0;}\
    else { if (mcallowbackprop ==0) {mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }}; }\
    else mcPROP_Z0; \
    DISALLOW_BACKPROP;\
  } while(0)

#define mcPROP_Z0 \
  do { \
    double mc_dt; \
    if(mcnlvz == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mc_dt = -mcnlz/mcnlvz; \
    if(mc_dt < 0 && mcallowbackprop == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mcPROP_DT(mc_dt); \
    mcnlz = 0; \
    DISALLOW_BACKPROP;\
  } while(0)

#define PROP_X0 \
  do { \
    if (mcgravitation) { Coords mcLocG; int mc_ret; \
    double mc_dt, mc_gx, mc_gy, mc_gz; \
    mcLocG = rot_apply(ROT_A_CURRENT_COMP, coords_set(0,-GRAVITY,0)); \
    coords_get(mcLocG, &mc_gx, &mc_gy, &mc_gz); \
    mc_ret = solve_2nd_order(&mc_dt, NULL, -mc_gx/2, -mcnlvx, -mcnlx); \
    if (mc_ret && mc_dt>=0) PROP_GRAV_DT(mc_dt, mc_gx, mc_gy, mc_gz); \
    else { if (mcallowbackprop ==0) {mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }}; }\
    else mcPROP_X0; \
    DISALLOW_BACKPROP;\
  } while(0)

#define mcPROP_X0 \
  do { \
    double mc_dt; \
    if(mcnlvx == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mc_dt = -mcnlx/mcnlvx; \
    if(mc_dt < 0 && mcallowbackprop == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mcPROP_DT(mc_dt); \
    mcnlx = 0; \
    DISALLOW_BACKPROP;\
  } while(0)

#define PROP_Y0 \
  do { \
    if (mcgravitation) { Coords mcLocG; int mc_ret; \
    double mc_dt, mc_gx, mc_gy, mc_gz; \
    mcLocG = rot_apply(ROT_A_CURRENT_COMP, coords_set(0,-GRAVITY,0)); \
    coords_get(mcLocG, &mc_gx, &mc_gy, &mc_gz); \
    mc_ret = solve_2nd_order(&mc_dt, NULL, -mc_gy/2, -mcnlvy, -mcnly); \
    if (mc_ret && mc_dt>=0) PROP_GRAV_DT(mc_dt, mc_gx, mc_gy, mc_gz); \
    else { if (mcallowbackprop ==0) {mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }}; }\
    else mcPROP_Y0; \
    DISALLOW_BACKPROP;\
  } while(0)


#define mcPROP_Y0 \
  do { \
    double mc_dt; \
    if(mcnlvy == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mc_dt = -mcnly/mcnlvy; \
    if(mc_dt < 0 && mcallowbackprop == 0) { mcAbsorbProp[INDEX_CURRENT_COMP]++; ABSORB; }; \
    mcPROP_DT(mc_dt); \
    mcnly = 0; \
    DISALLOW_BACKPROP; \
  } while(0)

/*moved from mccode-r.h*/
void mcsetstate(double x, double y, double z, double vx, double vy, double vz,
	double t, double sx, double sy, double sz, double p);

#ifdef DEBUG

#define mcDEBUG_STATE(x,y,z,vx,vy,vz,t,sx,sy,sz,p) if(!mcdotrace); else \
  printf("STATE: %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n", \
         x,y,z,vx,vy,vz,t,sx,sy,sz,p);
#define mcDEBUG_SCATTER(x,y,z,vx,vy,vz,t,sx,sy,sz,p) if(!mcdotrace); else \
  printf("SCATTER: %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n", \
         x,y,z,vx,vy,vz,t,sx,sy,sz,p);

#else

#define mcDEBUG_STATE(x,y,z,vx,vy,vz,t,sx,sy,sz,p)
#define mcDEBUG_SCATTER(x,y,z,vx,vy,vz,t,sx,sy,sz,p)

#endif

#endif /* !MCCODE_H */

#endif /* MCSTAS_R_H */
/* End of file "mcstas-r.h". */

#line 921 "/home/mcstas/test.c"

#line 1 "mccode-r.c"
/*******************************************************************************
*
* McCode, neutron/xray ray-tracing package
*         Copyright (C) 1997-2009, All rights reserved
*         Risoe National Laboratory, Roskilde, Denmark
*         Institut Laue Langevin, Grenoble, France
*
* Runtime: share/mccode-r.c
*
* %Identification
* Written by: KN
* Date:    Aug 29, 1997
* Release: McStas X.Y/McXtrace X.Y
* Version: $Revision$
*
* Runtime system for McStas and McXtrace.
* Embedded within instrument in runtime mode.
* Contains SECTIONS:
*   MPI handling (sum, send, recv)
*   format definitions
*   I/O
*   mcdisplay support
*   random numbers
*   coordinates handling
*   vectors math (solve 2nd order, normals, randvec...)
*   parameter handling
*   signal and main handlers
*
* Usage: Automatically embbeded in the c code whenever required.
*
* $Id$
*
*******************************************************************************/

/*******************************************************************************
* The I/O format definitions and functions
*******************************************************************************/


/** Include header files to avoid implicit declarations (not allowed on LLVM) */
#include <ctype.h>
#include <sys/types.h>

// UNIX specific headers (non-Windows)
#if defined(__unix__) || defined(__APPLE__)
#include <unistd.h>
#include <sys/stat.h>
#endif


#ifndef DANSE
#ifdef MC_ANCIENT_COMPATIBILITY
int mctraceenabled = 0;
int mcdefaultmain = 0;
#endif
/* else defined directly in the McCode generated C code */

static   long mcseed = 0; /* seed for random generator */
static   long mcstartdate = 0; /* start simulation time */
static   int  mcdisable_output_files = 0; /* --no-output-files */
mcstatic int  mcgravitation = 0; /* use gravitation flag, for PROP macros */
int      mcMagnet = 0; /* magnet stack flag */
mcstatic int  mcdotrace = 0; /* flag for --trace and messages for DISPLAY */
int      mcallowbackprop = 0;         /* flag to enable negative/backprop */

									  /* Number of particle histories to simulate. */
#ifdef NEUTRONICS
mcstatic unsigned long long int mcncount = 1;
mcstatic unsigned long long int mcrun_num = 0;
#else
mcstatic unsigned long long int mcncount = 1000000;
mcstatic unsigned long long int mcrun_num = 0;
#endif /* NEUTRONICS */

#else
#include "mcstas-globals.h"
#endif /* !DANSE */

/* SECTION: MPI handling ==================================================== */

#ifdef USE_MPI
/* MPI rank */
static int mpi_node_rank;
static int mpi_node_root = 0;


/*******************************************************************************
* mc_MPI_Reduce: Gathers arrays from MPI nodes using Reduce function.
*******************************************************************************/
int mc_MPI_Sum(double *sbuf, long count)
{
	if (!sbuf || count <= 0) return(MPI_SUCCESS); /* nothing to reduce */
	else {
		/* we must cut the buffer into blocks not exceeding the MPI max buffer size of 32000 */
		long   offset = 0;
		double *rbuf = NULL;
		int    length = MPI_REDUCE_BLOCKSIZE; /* defined in mccode-r.h */
		int    i = 0;
		rbuf = calloc(count, sizeof(double));
		if (!rbuf)
			exit(-fprintf(stderr, "Error: Out of memory %li (mc_MPI_Sum)\n", count * sizeof(double)));
		while (offset < count) {
			if (!length || offset + length > count - 1) length = count - offset;
			else length = MPI_REDUCE_BLOCKSIZE;
			if (MPI_Allreduce((double*)(sbuf + offset), (double*)(rbuf + offset),
				length, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD) != MPI_SUCCESS)
				return MPI_ERR_COUNT;
			offset += length;
		}

		for (i = 0; i<count; i++) sbuf[i] = rbuf[i];
		free(rbuf);
	}
	return MPI_SUCCESS;
} /* mc_MPI_Sum */

  /*******************************************************************************
  * mc_MPI_Send: Send array to MPI node by blocks to avoid buffer limit
  *******************************************************************************/
int mc_MPI_Send(void *sbuf,
	long count, MPI_Datatype dtype,
	int dest)
{
	int dsize;
	long offset = 0;
	int  tag = 1;
	int  length = MPI_REDUCE_BLOCKSIZE; /* defined in mccode-r.h */

	if (!sbuf || count <= 0) return(MPI_SUCCESS); /* nothing to send */
	MPI_Type_size(dtype, &dsize);

	while (offset < count) {
		if (offset + length > count - 1) length = count - offset;
		else length = MPI_REDUCE_BLOCKSIZE;
		if (MPI_Send((void*)(sbuf + offset*dsize), length, dtype, dest, tag++, MPI_COMM_WORLD) != MPI_SUCCESS)
			return MPI_ERR_COUNT;
		offset += length;
	}

	return MPI_SUCCESS;
} /* mc_MPI_Send */

  /*******************************************************************************
  * mc_MPI_Recv: Receives arrays from MPI nodes by blocks to avoid buffer limit
  *             the buffer must have been allocated previously.
  *******************************************************************************/
int mc_MPI_Recv(void *sbuf,
	long count, MPI_Datatype dtype,
	int source)
{
	int dsize;
	long offset = 0;
	int  tag = 1;
	int  length = MPI_REDUCE_BLOCKSIZE; /* defined in mccode-r.h */

	if (!sbuf || count <= 0) return(MPI_SUCCESS); /* nothing to recv */
	MPI_Type_size(dtype, &dsize);

	while (offset < count) {
		if (offset + length > count - 1) length = count - offset;
		else length = MPI_REDUCE_BLOCKSIZE;
		if (MPI_Recv((void*)(sbuf + offset*dsize), length, dtype, source, tag++,
			MPI_COMM_WORLD, MPI_STATUS_IGNORE) != MPI_SUCCESS)
			return MPI_ERR_COUNT;
		offset += length;
	}

	return MPI_SUCCESS;
} /* mc_MPI_Recv */

#endif /* USE_MPI */

  /* SECTION: parameters handling ============================================= */

  /* Instrument input parameter type handling. */
  /*******************************************************************************
  * mcparm_double: extract double value from 's' into 'vptr'
  *******************************************************************************/
static int
mcparm_double(char *s, void *vptr)
{
	char *p;
	double *v = (double *)vptr;

	if (!s) { *v = 0; return(1); }
	*v = strtod(s, &p);
	if (*s == '\0' || (p != NULL && *p != '\0') || errno == ERANGE)
		return 0;                        /* Failed */
	else
		return 1;                        /* Success */
}

/*******************************************************************************
* mcparminfo_double: display parameter type double
*******************************************************************************/
static char *
mcparminfo_double(char *parmname)
{
	return "double";
}

/*******************************************************************************
* mcparmerror_double: display error message when failed extract double
*******************************************************************************/
static void
mcparmerror_double(char *parm, char *val)
{
	fprintf(stderr, "Error: Invalid value '%s' for floating point parameter %s (mcparmerror_double)\n",
		val, parm);
}

/*******************************************************************************
* mcparmprinter_double: convert double to string
*******************************************************************************/
static void
mcparmprinter_double(char *f, void *vptr)
{
	double *v = (double *)vptr;
	sprintf(f, "%g", *v);
}

/*******************************************************************************
* mcparm_int: extract int value from 's' into 'vptr'
*******************************************************************************/
static int
mcparm_int(char *s, void *vptr)
{
	char *p;
	int *v = (int *)vptr;
	long x;

	if (!s) { *v = 0; return(1); }
	*v = 0;
	x = strtol(s, &p, 10);
	if (x < INT_MIN || x > INT_MAX)
		return 0;                        /* Under/overflow */
	*v = x;
	if (*s == '\0' || (p != NULL && *p != '\0') || errno == ERANGE)
		return 0;                        /* Failed */
	else
		return 1;                        /* Success */
}

/*******************************************************************************
* mcparminfo_int: display parameter type int
*******************************************************************************/
static char *
mcparminfo_int(char *parmname)
{
	return "int";
}

/*******************************************************************************
* mcparmerror_int: display error message when failed extract int
*******************************************************************************/
static void
mcparmerror_int(char *parm, char *val)
{
	fprintf(stderr, "Error: Invalid value '%s' for integer parameter %s (mcparmerror_int)\n",
		val, parm);
}

/*******************************************************************************
* mcparmprinter_int: convert int to string
*******************************************************************************/
static void
mcparmprinter_int(char *f, void *vptr)
{
	int *v = (int *)vptr;
	sprintf(f, "%d", *v);
}

/*******************************************************************************
* mcparm_string: extract char* value from 's' into 'vptr' (copy)
*******************************************************************************/
static int
mcparm_string(char *s, void *vptr)
{
	char **v = (char **)vptr;
	if (!s) { *v = NULL; return(1); }
	*v = (char *)malloc(strlen(s) + 1);
	if (*v == NULL)
	{
		exit(-fprintf(stderr, "Error: Out of memory %li (mcparm_string).\n", (long)strlen(s) + 1));
	}
	strcpy(*v, s);
	return 1;                        /* Success */
}

/*******************************************************************************
* mcparminfo_string: display parameter type string
*******************************************************************************/
static char *
mcparminfo_string(char *parmname)
{
	return "string";
}

/*******************************************************************************
* mcparmerror_string: display error message when failed extract string
*******************************************************************************/
static void
mcparmerror_string(char *parm, char *val)
{
	fprintf(stderr, "Error: Invalid value '%s' for string parameter %s (mcparmerror_string)\n",
		val, parm);
}

/*******************************************************************************
* mcparmprinter_string: convert string to string (including esc chars)
*******************************************************************************/
static void
mcparmprinter_string(char *f, void *vptr)
{
	char **v = (char **)vptr;
	char *p;

	if (!*v) { *f = '\0'; return; }
	strcpy(f, "");
	for (p = *v; *p != '\0'; p++)
	{
		switch (*p)
		{
		case '\n':
			strcat(f, "\\n");
			break;
		case '\r':
			strcat(f, "\\r");
			break;
		case '"':
			strcat(f, "\\\"");
			break;
		case '\\':
			strcat(f, "\\\\");
			break;
		default:
			strncat(f, p, 1);
		}
	}
	/* strcat(f, "\""); */
} /* mcparmprinter_string */

  /* now we may define the parameter structure, using previous functions */
static struct
{
	int(*getparm)(char *, void *);
	char * (*parminfo)(char *);
	void(*error)(char *, char *);
	void(*printer)(char *, void *);
} mcinputtypes[] = {
	{
		mcparm_double, mcparminfo_double, mcparmerror_double,
		mcparmprinter_double
	},{
		mcparm_int, mcparminfo_int, mcparmerror_int,
		mcparmprinter_int
	},{
		mcparm_string, mcparminfo_string, mcparmerror_string,
		mcparmprinter_string
	}
};

/*******************************************************************************
* mcestimate_error: compute sigma from N,p,p2 in Gaussian large numbers approx
*******************************************************************************/
double mcestimate_error(double N, double p1, double p2)
{
	double pmean, n1;
	if (N <= 1)
		return p1;
	pmean = p1 / N;
	n1 = N - 1;
	/* Note: underflow may cause p2 to become zero; the fabs() below guards
	against this. */
	return sqrt((N / n1)*fabs(p2 - pmean*pmean));
}

double(*mcestimate_error_p)
(double V2, double psum, double p2sum) = mcestimate_error;

/* ========================================================================== */

/*                               MCCODE_R_IO_C                                */

/* ========================================================================== */

#ifndef MCCODE_R_IO_C
#define MCCODE_R_IO_C "$Revision$"

/* SECTION: file i/o handling ================================================ */

#ifndef HAVE_STRCASESTR
// from msysgit: https://code.google.com/p/msysgit/source/browse/compat/strcasestr.c
char *strcasestr(const char *haystack, const char *needle)
{
	int nlen = strlen(needle);
	int hlen = strlen(haystack) - nlen + 1;
	int i;

	for (i = 0; i < hlen; i++) {
		int j;
		for (j = 0; j < nlen; j++) {
			unsigned char c1 = haystack[i + j];
			unsigned char c2 = needle[j];
			if (toupper(c1) != toupper(c2))
				goto next;
		}
		return (char *)haystack + i;
	next:
		;
	}
	return NULL;
}


#endif
#ifndef HAVE_STRCASECMP
int strcasecmp(const char *s1, const char *s2)
{
	int c1, c2;
	do {
		c1 = tolower((unsigned char)*s1++);
		c2 = tolower((unsigned char)*s2++);
	} while (c1 == c2 && c1 != 0);
	return c2 > c1 ? -1 : c1 > c2;
}
#endif

/*******************************************************************************
* mcfull_file: allocates a full file name=mcdirname+file. Catenate extension if missing.
*******************************************************************************/
char *mcfull_file(char *name, char *ext)
{
	int   dirlen = 0;
	char *mem = NULL;

	dirlen = mcdirname ? strlen(mcdirname) : 0;
	mem = (char*)malloc(dirlen + strlen(name) + CHAR_BUF_LENGTH);
	if (!mem) {
		exit(-fprintf(stderr, "Error: Out of memory %li (mcfull_file)\n", (long)(dirlen + strlen(name) + 256)));
	}
	strcpy(mem, "");

	/* prepend directory name to path if name does not contain a path */
	if (dirlen > 0 && !strchr(name, MC_PATHSEP_C)) {
		strcat(mem, mcdirname);
		strcat(mem, MC_PATHSEP_S);
	} /* dirlen */

	strcat(mem, name);
	if (!strchr(name, '.') && ext && strlen(ext))
	{ /* add extension if not in file name already */
		strcat(mem, ".");
		strcat(mem, ext);
	}
	return(mem);
} /* mcfull_file */

  /*******************************************************************************
  * mcnew_file: opens a new file within mcdirname if non NULL
  *             the file is opened in "a" (append, create if does not exist)
  *             the extension 'ext' is added if the file name does not include one.
  *             the last argument is set to 0 if file did not exist, else to 1.
  *******************************************************************************/
FILE *mcnew_file(char *name, char *ext, int *exists)
{
	char *mem;
	FILE *file = NULL;

	if (!name || strlen(name) == 0 || mcdisable_output_files) return(NULL);

	mem = mcfull_file(name, ext); /* create mcdirname/name.ext */

								  /* check for existence */
	file = fopen(mem, "r"); /* for reading -> fails if does not exist */
	if (file) {
		fclose(file);
		*exists = 1;
	}
	else
		*exists = 0;

	/* open the file for writing/appending */
#ifdef USE_NEXUS
	if (mcformat && strcasestr(mcformat, "NeXus")) {
		/* NXhandle nxhandle is defined in the .h with USE_NEXUS */
		NXaccess mode = (*exists ? NXACC_CREATE5 | NXACC_RDWR : NXACC_CREATE5);

		if (NXopen(mem, mode, &nxhandle) != NX_OK)
			file = NULL;
		else
			file = (FILE*)&nxhandle; /* to make it non NULL */
	}
	else
#endif
		file = fopen(mem, "a+");

	if (!file)
		fprintf(stderr, "Warning: could not open output file '%s' for %s (mcnew_file)\n",
			mem, *exists ? "append" : "create");
	free(mem);

	return file;
} /* mcnew_file */

  /*******************************************************************************
  * mcdetector_statistics: compute detector statistics, error bars, [x I I_err N] 1D
  * RETURN:            updated detector structure
  * Used by: mcdetector_import
  *******************************************************************************/
MCDETECTOR mcdetector_statistics(
	MCDETECTOR detector)
{

	if (!detector.p1 || !detector.m || !detector.filename)
		return(detector);

	/* compute statistics and update MCDETECTOR structure ===================== */
	double sum_z = 0, min_z = 0, max_z = 0;
	double fmon_x = 0, smon_x = 0, fmon_y = 0, smon_y = 0, mean_z = 0;
	double Nsum = 0, P2sum = 0;

	double sum_xz = 0, sum_yz = 0, sum_x = 0, sum_y = 0, sum_x2z = 0, sum_y2z = 0;
	int    i, j;
	char   hasnan = 0, hasinf = 0;
	char   israw = ((char*)strcasestr(detector.format, "raw") != NULL);
	double *this_p1 = NULL; /* new 1D McCode array [x I E N]. Freed after writing data */

							/* if McCode/PGPLOT and rank==1 we create a new m*4 data block=[x I E N] */
	if (detector.rank == 1 && strcasestr(detector.format, "McCode")) {
		this_p1 = (double *)calloc(detector.m*detector.n*detector.p * 4, sizeof(double));
		if (!this_p1)
			exit(-fprintf(stderr, "Error: Out of memory creating %li 1D " MCCODE_STRING " data set for file '%s' (mcdetector_import)\n",
				detector.m*detector.n*detector.p * 4 * sizeof(double*), detector.filename));
	}

	max_z = min_z = detector.p1[0];

	/* compute sum and moments (not for lists) */
	if (!strcasestr(detector.format, "list") && detector.m)
		for (j = 0; j < detector.n*detector.p; j++)
		{
			for (i = 0; i < detector.m; i++)
			{
				double x, y, z;
				double N, E;
				long   index = !detector.istransposed ? i*detector.n*detector.p + j : i + j*detector.m;
				char   hasnaninf = 0;

				if (detector.m)
					x = detector.xmin + (i + 0.5) / detector.m*(detector.xmax - detector.xmin);
				else x = 0;
				if (detector.n && detector.p)
					y = detector.ymin + (j + 0.5) / detector.n / detector.p*(detector.ymax - detector.ymin);
				else y = 0;
				z = detector.p1[index];
				N = detector.p0 ? detector.p0[index] : 1;
				E = detector.p2 ? detector.p2[index] : 0;
				if (detector.p2 && !israw)
					detector.p2[index] = (*mcestimate_error_p)(detector.p0[index], detector.p1[index], detector.p2[index]); /* set sigma */

				if (detector.rank == 1 && this_p1 && strcasestr(detector.format, "McCode")) {
					/* fill-in 1D McCode array [x I E N] */
					this_p1[index * 4] = x;
					this_p1[index * 4 + 1] = z;
					this_p1[index * 4 + 2] = detector.p2 ? detector.p2[index] : 0;
					this_p1[index * 4 + 3] = N;
				}

				if (isnan(z) || isnan(E) || isnan(N)) hasnaninf = hasnan = 1;
				if (isinf(z) || isinf(E) || isinf(N)) hasnaninf = hasinf = 1;

				/* compute stats integrals */
				if (!hasnaninf) {
					sum_xz += x*z;
					sum_yz += y*z;
					sum_x += x;
					sum_y += y;
					sum_z += z;
					sum_x2z += x*x*z;
					sum_y2z += y*y*z;
					if (z > max_z) max_z = z;
					if (z < min_z) min_z = z;

					Nsum += N;
					P2sum += E;
				}

			}
		} /* for j */

		  /* compute 1st and 2nd moments. For lists, sum_z=0 so this is skipped. */
	if (sum_z && detector.n*detector.m*detector.p)
	{
		fmon_x = sum_xz / sum_z;
		fmon_y = sum_yz / sum_z;
		smon_x = sum_x2z / sum_z - fmon_x*fmon_x; smon_x = smon_x > 0 ? sqrt(smon_x) : 0;
		smon_y = sum_y2z / sum_z - fmon_y*fmon_y; smon_y = smon_y > 0 ? sqrt(smon_y) : 0;
		mean_z = sum_z / detector.n / detector.m / detector.p;
	}
	/* store statistics into detector */
	detector.intensity = sum_z;
	detector.error = Nsum ? (*mcestimate_error_p)(Nsum, sum_z, P2sum) : 0;
	detector.events = Nsum;
	detector.min = min_z;
	detector.max = max_z;
	detector.mean = mean_z;
	detector.centerX = fmon_x;
	detector.halfwidthX = smon_x;
	detector.centerY = fmon_y;
	detector.halfwidthY = smon_y;

	/* if McCode/PGPLOT and rank==1 replace p1 with new m*4 1D McCode and clear others */
	if (detector.rank == 1 && this_p1 && strcasestr(detector.format, "McCode")) {

		detector.p1 = this_p1;
		detector.n = detector.m; detector.m = 4;
		detector.p0 = detector.p2 = NULL;
		detector.istransposed = 1;
	}

	if (detector.n*detector.m*detector.p > 1)
		snprintf(detector.signal, CHAR_BUF_LENGTH,
			"Min=%g; Max=%g; Mean=%g;", detector.min, detector.max, detector.mean);
	else
		strcpy(detector.signal, "None");
	snprintf(detector.values, CHAR_BUF_LENGTH,
		"%g %g %g", detector.intensity, detector.error, detector.events);

	switch (detector.rank) {
	case 1:  snprintf(detector.statistics, CHAR_BUF_LENGTH, "X0=%g; dX=%g;",
		detector.centerX, detector.halfwidthX); break;
	case 2:
	case 3:  snprintf(detector.statistics, CHAR_BUF_LENGTH, "X0=%g; dX=%g; Y0=%g; dY=%g;",
		detector.centerX, detector.halfwidthX, detector.centerY, detector.halfwidthY);
		break;
	default: strcpy(detector.statistics, "None");
	}

	if (hasnan)
		printf("WARNING: Nan detected in component/file %s %s\n",
			detector.component, strlen(detector.filename) ? detector.filename : "");
	if (hasinf)
		printf("WARNING: Inf detected in component/file %s %s\n",
			detector.component, strlen(detector.filename) ? detector.filename : "");

	return(detector);

} /* mcdetector_statistics */

  /*******************************************************************************
  * mcdetector_import: build detector structure, merge non-lists from MPI
  *                    compute basic stat, write "Detector:" line
  * RETURN:            detector structure. Invalid data if detector.p1 == NULL
  *                    Invalid detector sets m=0 and filename=""
  *                    Simulation data  sets m=0 and filename=mcsiminfo_name
  * This function is equivalent to the old 'mcdetector_out', returning a structure
  *******************************************************************************/
MCDETECTOR mcdetector_import(
	char *format,
	char *component, char *title,
	long m, long n, long p,
	char *xlabel, char *ylabel, char *zlabel,
	char *xvar, char *yvar, char *zvar,
	double x1, double x2, double y1, double y2, double z1, double z2,
	char *filename,
	double *p0, double *p1, double *p2,
	Coords position)
{
	time_t t;       /* for detector.date */
	long   date_l;  /* date as a long number */
	char   istransposed = 0;
	char   c[CHAR_BUF_LENGTH]; /* temp var for signal label */

	MCDETECTOR detector;

	/* build MCDETECTOR structure ============================================= */
	/* make sure we do not have NULL for char fields */

	/* these also apply to simfile */
	strncpy(detector.filename, filename ? filename : "", CHAR_BUF_LENGTH);
	strncpy(detector.format, format ? format : "McCode", CHAR_BUF_LENGTH);
	/* add extension if missing */
	if (strlen(detector.filename) && !strchr(detector.filename, '.'))
	{ /* add extension if not in file name already */
		strcat(detector.filename, ".dat");
	}
	strncpy(detector.component, component ? component : MCCODE_STRING " component", CHAR_BUF_LENGTH);

	snprintf(detector.instrument, CHAR_BUF_LENGTH, "%s (%s)", mcinstrument_name, mcinstrument_source);
	snprintf(detector.user, CHAR_BUF_LENGTH, "%s on %s",
		getenv("USER") ? getenv("USER") : MCCODE_NAME,
		getenv("HOST") ? getenv("HOST") : "localhost");
	time(&t);         /* get current write time */
	date_l = (long)t; /* same but as a long */
	snprintf(detector.date, CHAR_BUF_LENGTH, "%s", ctime(&t));
	if (strlen(detector.date))   detector.date[strlen(detector.date) - 1] = '\0'; /* remove last \n in date */
	detector.date_l = date_l;

	if (!mcget_run_num() || mcget_run_num() >= mcget_ncount())
		snprintf(detector.ncount, CHAR_BUF_LENGTH, "%llu", mcget_ncount()
#ifdef USE_MPI
			*mpi_node_count
#endif
		);
	else
		snprintf(detector.ncount, CHAR_BUF_LENGTH, "%g/%g", (double)mcget_run_num(), (double)mcget_ncount());

	detector.p0 = p0;
	detector.p1 = p1;
	detector.p2 = p2;

	/* handle transposition (not for NeXus) */
	if (!strcasestr(detector.format, "NeXus")) {
		if (m<0 || n<0 || p<0)             istransposed = !istransposed;
		if (strcasestr(detector.format, "transpose")) istransposed = !istransposed;
		if (istransposed) { /* do the swap once for all */
			long i = m; m = n; n = i;
		}
	}

	m = abs(m); n = abs(n); p = abs(p); /* make sure dimensions are positive */
	detector.istransposed = istransposed;

	/* determine detector rank (dimensionality) */
	if (!m || !n || !p || !p1) detector.rank = 4; /* invalid: exit with m=0 filename="" */
	else if (m*n*p == 1)       detector.rank = 0; /* 0D */
	else if (n == 1 || m == 1) detector.rank = 1; /* 1D */
	else if (p == 1)           detector.rank = 2; /* 2D */
	else                       detector.rank = 3; /* 3D */

												  /* from rank, set type */
	switch (detector.rank) {
	case 0:  strcpy(detector.type, "array_0d"); m = n = p = 1; break;
	case 1:  snprintf(detector.type, CHAR_BUF_LENGTH, "array_1d(%ld)", m*n*p); m *= n*p; n = p = 1; break;
	case 2:  snprintf(detector.type, CHAR_BUF_LENGTH, "array_2d(%ld, %ld)", m, n*p); n *= p; p = 1; break;
	case 3:  snprintf(detector.type, CHAR_BUF_LENGTH, "array_3d(%ld, %ld, %ld)", m, n, p); break;
	default: m = 0; strcpy(detector.type, ""); strcpy(detector.filename, "");/* invalid */
	}

	detector.m = m;
	detector.n = n;
	detector.p = p;

	/* these only apply to detector files ===================================== */

	snprintf(detector.position, CHAR_BUF_LENGTH, "%g %g %g", position.x, position.y, position.z);
	/* may also store actual detector orientation in the future */

	strncpy(detector.title, title && strlen(title) ? title : component, CHAR_BUF_LENGTH);
	strncpy(detector.xlabel, xlabel && strlen(xlabel) ? xlabel : "X", CHAR_BUF_LENGTH); /* axis labels */
	strncpy(detector.ylabel, ylabel && strlen(ylabel) ? ylabel : "Y", CHAR_BUF_LENGTH);
	strncpy(detector.zlabel, zlabel && strlen(zlabel) ? zlabel : "Z", CHAR_BUF_LENGTH);
	strncpy(detector.xvar, xvar && strlen(xvar) ? xvar : "x", CHAR_BUF_LENGTH); /* axis variables */
	strncpy(detector.yvar, yvar && strlen(yvar) ? yvar : detector.xvar, CHAR_BUF_LENGTH);
	strncpy(detector.zvar, zvar && strlen(zvar) ? zvar : detector.yvar, CHAR_BUF_LENGTH);

	/* set "variables" as e.g. "I I_err N" */
	strcpy(c, "I ");
	if (strlen(detector.zvar))      strncpy(c, detector.zvar, 32);
	else if (strlen(detector.yvar)) strncpy(c, detector.yvar, 32);
	else if (strlen(detector.xvar)) strncpy(c, detector.xvar, 32);

	if (detector.rank == 1)
		snprintf(detector.variables, CHAR_BUF_LENGTH, "%s %s %s_err N", detector.xvar, c, c);
	else
		snprintf(detector.variables, CHAR_BUF_LENGTH, "%s %s_err N", c, c);

	/* limits */
	detector.xmin = x1;
	detector.xmax = x2;
	detector.ymin = y1;
	detector.ymax = y2;
	detector.zmin = z1;
	detector.zmax = z2;
	if (abs(detector.rank) == 1)
		snprintf(detector.limits, CHAR_BUF_LENGTH, "%g %g", x1, x2);
	else if (detector.rank == 2)
		snprintf(detector.limits, CHAR_BUF_LENGTH, "%g %g %g %g", x1, x2, y1, y2);
	else
		snprintf(detector.limits, CHAR_BUF_LENGTH, "%g %g %g %g %g %g", x1, x2, y1, y2, z1, z2);

	/* if MPI and nodes_nb > 1: reduce data sets when using MPI =============== */
#ifdef USE_MPI
	if (!strcasestr(detector.format, "list") && mpi_node_count > 1 && m) {
		/* we save additive data: reduce everything into mpi_node_root */
		if (p0) mc_MPI_Sum(p0, m*n*p);
		if (p1) mc_MPI_Sum(p1, m*n*p);
		if (p2) mc_MPI_Sum(p2, m*n*p);
		if (!p0) {  /* additive signal must be then divided by the number of nodes */
			int i;
			for (i = 0; i<m*n*p; i++) {
				p1[i] /= mpi_node_count;
				if (p2) p2[i] /= mpi_node_count;
			}
		}
	}
#endif /* USE_MPI */

	/* compute statistics, Nsum, intensity, Error bars */
	detector = mcdetector_statistics(detector);

#ifdef USE_MPI
	/* slaves are done */
	if (mpi_node_rank != mpi_node_root) {
		return detector;
	}
#endif

	/* output "Detector:" line ================================================ */
	/* when this is a detector written by a component (not the SAVE from instrument),
	not an event lists */
	if (!m) return(detector);
	if (!strcasestr(detector.format, "list")) {
		if (!strcmp(detector.component, mcinstrument_name)) {
			if (strlen(detector.filename))  /* we name it from its filename, or from its title */
				strncpy(c, detector.filename, CHAR_BUF_LENGTH);
			else
				snprintf(c, CHAR_BUF_LENGTH, "%s", mcinstrument_name);
		}
		else
			strncpy(c, detector.component, CHAR_BUF_LENGTH);  /* usual detectors written by components */

		printf("Detector: %s_I=%g %s_ERR=%g %s_N=%g",
			c, detector.intensity,
			c, detector.error,
			c, detector.events);
		printf(" \"%s\"\n", strlen(detector.filename) ? detector.filename : detector.component);
	}


	return(detector);
} /* mcdetector_import */

  /* end MCDETECTOR import section ============================================ */

















  /* ========================================================================== */

  /*                               ASCII output                                 */
  /*     The SIM file is YAML based, the data files have '#' headers            */

  /* ========================================================================== */


  /*******************************************************************************
  * mcinfo_out: output instrument tags/info (only in SIM)
  * Used in: mcsiminfo_init (ascii), mcinfo(stdout)
  *******************************************************************************/
static void mcinfo_out(char *pre, FILE *f)
{
	char Parameters[CHAR_BUF_LENGTH] = "";
	int  i;

	if (!f || mcdisable_output_files) return;

	/* create parameter string ================================================ */
	for (i = 0; i < mcnumipar; i++)
	{
		char ThisParam[CHAR_BUF_LENGTH];
		if (strlen(mcinputtable[i].name) > CHAR_BUF_LENGTH) break;
		snprintf(ThisParam, CHAR_BUF_LENGTH, " %s(%s)", mcinputtable[i].name,
			(*mcinputtypes[mcinputtable[i].type].parminfo)
			(mcinputtable[i].name));
		strcat(Parameters, ThisParam);
		if (strlen(Parameters) >= CHAR_BUF_LENGTH - 64) break;
	}

	/* output data ============================================================ */
	if (f != stdout)
		fprintf(f, "%sFile: %s%c%s\n", pre, mcdirname, MC_PATHSEP_C, mcsiminfo_name);
	else
		fprintf(f, "%sCreator: %s\n", pre, MCCODE_STRING);

	fprintf(f, "%sSource: %s\n", pre, mcinstrument_source);
	fprintf(f, "%sParameters: %s\n", pre, Parameters);

	fprintf(f, "%sTrace_enabled: %s\n", pre, mctraceenabled ? "yes" : "no");
	fprintf(f, "%sDefault_main: %s\n", pre, mcdefaultmain ? "yes" : "no");
	fprintf(f, "%sEmbedded_runtime: %s\n", pre,
#ifdef MC_EMBEDDED_RUNTIME
		"yes"
#else
		"no"
#endif
	);

	fflush(f);
} /* mcinfo_out */

  /*******************************************************************************
  * mcruninfo_out: output simulation tags/info (both in SIM and data files)
  * Used in: mcsiminfo_init (ascii case), mcdetector_out_xD_ascii
  *******************************************************************************/
static void mcruninfo_out(char *pre, FILE *f)
{
	int i;
	char Parameters[CHAR_BUF_LENGTH];

	if (!f || mcdisable_output_files) return;

	fprintf(f, "%sFormat: %s%s\n", pre,
		mcformat && strlen(mcformat) ? mcformat : MCCODE_NAME,
		mcformat && strcasestr(mcformat, "McCode") ? " with text headers" : "");
	fprintf(f, "%sURL: %s\n", pre, "http://www.mccode.org");
	fprintf(f, "%sCreator: %s\n", pre, MCCODE_STRING);
	fprintf(f, "%sInstrument: %s\n", pre, mcinstrument_source);
	fprintf(f, "%sNcount: %llu\n", pre, mcget_ncount());
	fprintf(f, "%sTrace: %s\n", pre, mcdotrace ? "yes" : "no");
	fprintf(f, "%sGravitation: %s\n", pre, mcgravitation ? "yes" : "no");
	snprintf(Parameters, CHAR_BUF_LENGTH, "%ld", mcseed);
	fprintf(f, "%sSeed: %s\n", pre, Parameters);
	fprintf(f, "%sDirectory: %s\n", pre, mcdirname ? mcdirname : ".");
#ifdef USE_MPI
	if (mpi_node_count > 1)
		fprintf(f, "%sNodes: %i\n", pre, mpi_node_count);
#endif

	/* output parameter string ================================================ */
	for (i = 0; i < mcnumipar; i++) {
		if (mcget_run_num() || (mcinputtable[i].val && strlen(mcinputtable[i].val))) {
			if (mcinputtable[i].par == NULL)
				strncpy(Parameters, (mcinputtable[i].val ? mcinputtable[i].val : ""), CHAR_BUF_LENGTH);
			else
				(*mcinputtypes[mcinputtable[i].type].printer)(Parameters, mcinputtable[i].par);

			fprintf(f, "%sParam: %s=%s\n", pre, mcinputtable[i].name, Parameters);
		}
	}
	fflush(f);
} /* mcruninfo_out */

  /*******************************************************************************
  * mcsiminfo_out:    wrapper to fprintf(mcsiminfo_file)
  *******************************************************************************/
void mcsiminfo_out(char *format, ...)
{
	va_list ap;

	if (mcsiminfo_file && !mcdisable_output_files)
	{
		va_start(ap, format);
		vfprintf(mcsiminfo_file, format, ap);
		va_end(ap);
	}
} /* mcsiminfo_out */


  /*******************************************************************************
  * mcdatainfo_out: output detector header
  *   mcdatainfo_out(prefix, file_handle, detector) writes info to data file
  *******************************************************************************/
static void
mcdatainfo_out(char *pre, FILE *f, MCDETECTOR detector)
{
	if (!f || !detector.m || mcdisable_output_files) return;

	/* output data ============================================================ */
	fprintf(f, "%sDate: %s (%li)\n", pre, detector.date, detector.date_l);
	fprintf(f, "%stype: %s\n", pre, detector.type);
	fprintf(f, "%sSource: %s\n", pre, detector.instrument);
	fprintf(f, "%scomponent: %s\n", pre, detector.component);
	fprintf(f, "%sposition: %s\n", pre, detector.position);

	fprintf(f, "%stitle: %s\n", pre, detector.title);
	fprintf(f, !mcget_run_num() || mcget_run_num() >= mcget_ncount() ?
		"%sNcount: %s\n" :
		"%sratio: %s\n", pre, detector.ncount);

	if (strlen(detector.filename)) {
		fprintf(f, "%sfilename: %s\n", pre, detector.filename);
	}

	fprintf(f, "%sstatistics: %s\n", pre, detector.statistics);
	fprintf(f, "%ssignal: %s\n", pre, detector.signal);
	fprintf(f, "%svalues: %s\n", pre, detector.values);

	if (detector.rank >= 1)
	{
		fprintf(f, "%sxvar: %s\n", pre, detector.xvar);
		fprintf(f, "%syvar: %s\n", pre, detector.yvar);
		fprintf(f, "%sxlabel: %s\n", pre, detector.xlabel);
		fprintf(f, "%sylabel: %s\n", pre, detector.ylabel);
		if (detector.rank > 1) {
			fprintf(f, "%szvar: %s\n", pre, detector.zvar);
			fprintf(f, "%szlabel: %s\n", pre, detector.zlabel);
		}
	}

	fprintf(f,
		abs(detector.rank) == 1 ?
		"%sxlimits: %s\n" :
		"%sxylimits: %s\n", pre, detector.limits);
	fprintf(f, "%svariables: %s\n", pre,
		strcasestr(detector.format, "list") ? detector.ylabel : detector.variables);

	fflush(f);

} /* mcdatainfo_out */

  /* mcdetector_out_array_ascii: output a single array to a file
  *   m: columns
  *   n: rows
  *   p: array
  *   f: file handle (already opened)
  */
static void mcdetector_out_array_ascii(long m, long n, double *p, FILE *f, char istransposed)
{
	if (f)
	{
		int i, j;
		for (j = 0; j < n; j++)
		{
			for (i = 0; i < m; i++)
			{
				fprintf(f, "%g ", p[!istransposed ? i*n + j : j*m + i]);
			}
			fprintf(f, "\n");
		}
	}
} /* mcdetector_out_array_ascii */

  /*******************************************************************************
  * mcdetector_out_0D_ascii: called by mcdetector_out_0D for ascii output
  *******************************************************************************/
MCDETECTOR mcdetector_out_0D_ascii(MCDETECTOR detector)
{
	int exists = 0;
	FILE *outfile = NULL;

	/* Write data set information to simulation description file. */
	MPI_MASTER(
		mcsiminfo_out("\nbegin data\n"); // detector.component
	mcdatainfo_out("  ", mcsiminfo_file, detector);
	mcsiminfo_out("end data\n");
	/* Don't write if filename is NULL: mcnew_file handles this (return NULL) */
	outfile = mcnew_file(detector.component, "dat", &exists);
	if (outfile)
	{
		/* write data file header and entry in simulation description file */
		mcruninfo_out("# ", outfile);
		mcdatainfo_out("# ", outfile, detector);
		/* write I I_err N */
		fprintf(outfile, "%g %g %g\n",
			detector.intensity, detector.error, detector.events);
		fclose(outfile);
	}
	); /* MPI_MASTER */
	return(detector);
} /* mcdetector_out_0D_ascii */

  /*******************************************************************************
  * mcdetector_out_1D_ascii: called by mcdetector_out_1D for ascii output
  *******************************************************************************/
MCDETECTOR mcdetector_out_1D_ascii(MCDETECTOR detector)
{
	int exists = 0;
	FILE *outfile = NULL;

	MPI_MASTER(
		/* Write data set information to simulation description file. */
		mcsiminfo_out("\nbegin data\n"); // detector.filename
	mcdatainfo_out("  ", mcsiminfo_file, detector);
	mcsiminfo_out("end data\n");
	/* Loop over array elements, writing to file. */
	/* Don't write if filename is NULL: mcnew_file handles this (return NULL) */
	outfile = mcnew_file(detector.filename, "dat", &exists);
	if (outfile)
	{
		/* write data file header and entry in simulation description file */
		mcruninfo_out("# ", outfile);
		mcdatainfo_out("# ", outfile, detector);
		/* output the 1D array columns */
		mcdetector_out_array_ascii(detector.m, detector.n, detector.p1, outfile, detector.istransposed);

		fclose(outfile);
	}
	); /* MPI_MASTER */
	return(detector);

}  /* mcdetector_out_1D_ascii */

   /*******************************************************************************
   * mcdetector_out_2D_ascii: called by mcdetector_out_2D for ascii output
   *******************************************************************************/
MCDETECTOR mcdetector_out_2D_ascii(MCDETECTOR detector)
{
	int exists = 0;
	FILE *outfile = NULL;

	MPI_MASTER(
		/* Loop over array elements, writing to file. */
		/* Don't write if filename is NULL: mcnew_file handles this (return NULL) */
		outfile = mcnew_file(detector.filename, "dat", &exists);
	if (outfile)
	{
		/* write header only if file has just been created (not appending) */
		if (!exists) {
			/* Write data set information to simulation description file. */
			mcsiminfo_out("\nbegin data\n"); // detector.filename
			mcdatainfo_out("  ", mcsiminfo_file, detector);
			mcsiminfo_out("end data\n");

			mcruninfo_out("# ", outfile);
			mcdatainfo_out("# ", outfile, detector);
			fprintf(outfile, "# Data [%s/%s] %s:\n", detector.component, detector.filename, detector.zvar);
		}
		mcdetector_out_array_ascii(detector.m, detector.n*detector.p, detector.p1,
			outfile, detector.istransposed);
		if (detector.p2) {
			fprintf(outfile, "# Errors [%s/%s] %s_err:\n", detector.component, detector.filename, detector.zvar);
			mcdetector_out_array_ascii(detector.m, detector.n*detector.p, detector.p2,
				outfile, detector.istransposed);
		}
		if (detector.p0) {
			fprintf(outfile, "# Events [%s/%s] N:\n", detector.component, detector.filename);
			mcdetector_out_array_ascii(detector.m, detector.n*detector.p, detector.p0,
				outfile, detector.istransposed);
		}
		fclose(outfile);

		if (!exists) {
			if (strcasestr(detector.format, "list"))
				printf("Events:   \"%s\"\n",
					strlen(detector.filename) ? detector.filename : detector.component);
		}
	} /* if outfile */
	); /* MPI_MASTER */
#ifdef USE_MPI
	if (strcasestr(detector.format, "list") && mpi_node_count > 1) {
		int node_i = 0;
		/* loop along MPI nodes to write sequentially */
		for (node_i = 0; node_i<mpi_node_count; node_i++) {
			/* MPI: slaves wait for the master to write its block, then append theirs */
			MPI_Barrier(MPI_COMM_WORLD);
			if (node_i != mpi_node_root && node_i == mpi_node_rank) {
				if (strlen(detector.filename) && !mcdisable_output_files)	/* Don't write if filename is NULL */
					outfile = mcnew_file(detector.filename, "dat", &exists);
				if (!exists)
					fprintf(stderr, "Warning: [MPI node %i] file '%s' does not exist yet, "
						"MASTER should have opened it before.\n",
						mpi_node_rank, detector.filename);
				if (outfile) {
					mcdetector_out_array_ascii(detector.m, detector.n*detector.p, detector.p1,
						outfile, detector.istransposed);
					fclose(outfile);
				}
			}
		}
	} /* if strcasestr list */
#endif
	return(detector);
} /* mcdetector_out_2D_ascii */

  /*******************************************************************************
  * strcpy_valid: makes a valid string for variable names.
  *   copy 'original' into 'valid', replacing invalid characters by '_'
  *   char arrays must be pre-allocated
  *******************************************************************************/
static char *strcpy_valid(char *valid, char *original)
{
	long i;
	int  n = 32; /* max length of valid names */

	if (original == NULL || !strlen(original)) return(NULL);

	if (n > strlen(original)) n = strlen(original);
	else original += strlen(original) - n;
	strncpy(valid, original, n);

	for (i = 0; i < n; i++)
	{
		if ((valid[i] > 122)
			|| (valid[i] < 32)
			|| (strchr("!\"#$%&'()*+,-.:;<=>?@[\\]^`/ \n\r\t", valid[i]) != NULL))
		{
			if (i) valid[i] = '_'; else valid[i] = 'm';
		}
	}
	valid[i] = '\0';

	return(valid);
} /* strcpy_valid */

  /* end ascii output section ================================================= */







#ifdef USE_NEXUS

  /* ========================================================================== */

  /*                               NeXus output                                 */

  /* ========================================================================== */

#define nxprintf(...)    nxstr('d', __VA_ARGS__)
#define nxprintattr(...) nxstr('a', __VA_ARGS__)

  /*******************************************************************************
  * nxstr: output a tag=value data set (char) in NeXus/current group
  *   when 'format' is larger that 1024 chars it is used as value for the 'tag'
  *   else the value is assembled with format and following arguments.
  *   type='d' -> data set
  *        'a' -> attribute for current data set
  *******************************************************************************/
static int nxstr(char type, NXhandle *f, char *tag, char *format, ...)
{
	va_list ap;
	char value[CHAR_BUF_LENGTH];
	int  i;
	int  ret = NX_OK;

	if (!tag || !format || !strlen(tag) || !strlen(format)) return(NX_OK);

	/* assemble the value string */
	if (strlen(format) < CHAR_BUF_LENGTH) {
		va_start(ap, format);
		ret = vsnprintf(value, CHAR_BUF_LENGTH, format, ap);
		va_end(ap);

		i = strlen(value);
	}
	else {
		i = strlen(format);
	}

	if (type == 'd') {
		/* open/put/close data set */
		if (NXmakedata(f, tag, NX_CHAR, 1, &i) != NX_OK) return(NX_ERROR);
		NXopendata(f, tag);
		if (strlen(format) < CHAR_BUF_LENGTH)
			ret = NXputdata(f, value);
		else
			ret = NXputdata(f, format);
		NXclosedata(f);
	}
	else {
		if (strlen(format) < CHAR_BUF_LENGTH)
			ret = NXputattr(f, tag, value, strlen(value), NX_CHAR);
		else
			ret = NXputattr(f, tag, format, strlen(format), NX_CHAR);
	}

	return(ret);

} /* nxstr */

  /*******************************************************************************
  * mcinfo_readfile: read a full file into a string buffer which is allocated
  *   Think to free the buffer after use.
  * Used in: mcinfo_out_nexus (nexus)
  *******************************************************************************/
char *mcinfo_readfile(char *filename)
{
	FILE *f = fopen(filename, "r");
	if (!f) return(NULL);
	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);
	rewind(f);
	char *string = malloc(fsize + 1);
	if (string) {
		int n = fread(string, fsize, 1, f);
		fclose(f);

		string[fsize] = 0;
	}
	return(string);
}

/*******************************************************************************
* mcinfo_out: output instrument/simulation groups in NeXus file
* Used in: mcsiminfo_init (nexus)
*******************************************************************************/
static void mcinfo_out_nexus(NXhandle f)
{
	FILE  *fid;     /* for intrument source code/C/IDF */
	char  *buffer = NULL;
	time_t t = time(NULL); /* for date */
	char   entry0[CHAR_BUF_LENGTH];
	int    count = 0;
	char   name[CHAR_BUF_LENGTH];
	char   class[CHAR_BUF_LENGTH];

	if (!f || mcdisable_output_files) return;

	/* write NeXus NXroot attributes */
	/* automatically added: file_name, HDF5_Version, file_time, NeXus_version */
	nxprintattr(f, "creator", "%s generated with " MCCODE_STRING, mcinstrument_name);

	/* count the number of existing NXentry and create the next one */
	NXgetgroupinfo(f, &count, name, class);
	sprintf(entry0, "entry%i", count + 1);

	/* create the main NXentry (mandatory in NeXus) */
	if (NXmakegroup(f, entry0, "NXentry") == NX_OK)
		if (NXopengroup(f, entry0, "NXentry") == NX_OK) {

			nxprintf(nxhandle, "program_name", MCCODE_STRING);
			nxprintf(f, "start_time", ctime(&t));
			nxprintf(f, "title", "%s%s%s simulation generated by instrument %s",
				mcdirname && strlen(mcdirname) ? mcdirname : ".", MC_PATHSEP_S, mcsiminfo_name,
				mcinstrument_name);
			nxprintattr(f, "program_name", MCCODE_STRING);
			nxprintattr(f, "instrument", mcinstrument_name);
			nxprintattr(f, "simulation", "%s%s%s",
				mcdirname && strlen(mcdirname) ? mcdirname : ".", MC_PATHSEP_S, mcsiminfo_name);

			/* write NeXus instrument group */
			if (NXmakegroup(f, "instrument", "NXinstrument") == NX_OK)
				if (NXopengroup(f, "instrument", "NXinstrument") == NX_OK) {
					int   i;
					char *string = NULL;

					/* write NeXus parameters(types) data =================================== */
					string = (char*)malloc(CHAR_BUF_LENGTH);
					if (string) {
						strcpy(string, "");
						for (i = 0; i < mcnumipar; i++)
						{
							char ThisParam[CHAR_BUF_LENGTH];
							snprintf(ThisParam, CHAR_BUF_LENGTH, " %s(%s)", mcinputtable[i].name,
								(*mcinputtypes[mcinputtable[i].type].parminfo)
								(mcinputtable[i].name));
							if (strlen(string) + strlen(ThisParam) < CHAR_BUF_LENGTH)
								strcat(string, ThisParam);
						}
						nxprintattr(f, "Parameters", string);
						free(string);
					}

					nxprintattr(f, "name", mcinstrument_name);
					nxprintf(f, "name", mcinstrument_name);
					nxprintattr(f, "Source", mcinstrument_source);

					nxprintattr(f, "Trace_enabled", mctraceenabled ? "yes" : "no");
					nxprintattr(f, "Default_main", mcdefaultmain ? "yes" : "no");
					nxprintattr(f, "Embedded_runtime",
#ifdef MC_EMBEDDED_RUNTIME
						"yes"
#else
						"no"
#endif
					);

					/* add instrument source code when available */
					buffer = mcinfo_readfile(mcinstrument_source);
					if (buffer && strlen(buffer)) {
						long length = strlen(buffer);
						nxprintf(f, "description", buffer);
						NXopendata(f, "description");
						nxprintattr(f, "file_name", mcinstrument_source);
						nxprintattr(f, "file_size", "%li", length);
						nxprintattr(f, "MCCODE_STRING", MCCODE_STRING);
						NXclosedata(f);
						nxprintf(f, "instrument_source", "%s " MCCODE_NAME " " MCCODE_PARTICLE " Monte Carlo simulation", mcinstrument_name);
						free(buffer);
					}
					else
						nxprintf(f, "description", "File %s not found (instrument description %s is missing)",
							mcinstrument_source, mcinstrument_name);

					/* add Mantid/IDF.xml when available */
					char *IDFfile = NULL;
					IDFfile = (char*)malloc(CHAR_BUF_LENGTH);
					sprintf(IDFfile, "%s%s", mcinstrument_source, ".xml");
					buffer = mcinfo_readfile(IDFfile);
					if (buffer && strlen(buffer)) {
						NXmakegroup(nxhandle, "instrument_xml", "NXnote");
						NXopengroup(nxhandle, "instrument_xml", "NXnote");
						nxprintf(f, "data", buffer);
						nxprintf(f, "description", "IDF.xml file found with instrument %s", mcinstrument_source);
						nxprintf(f, "type", "text/xml");
						NXclosegroup(f); /* instrument_xml */
						free(buffer);
					}
					free(IDFfile);
					NXclosegroup(f); /* instrument */
				} /* NXinstrument */

				  /* write NeXus simulation group */
			if (NXmakegroup(f, "simulation", "NXnote") == NX_OK)
				if (NXopengroup(f, "simulation", "NXnote") == NX_OK) {

					nxprintattr(f, "name", "%s%s%s",
						mcdirname && strlen(mcdirname) ? mcdirname : ".", MC_PATHSEP_S, mcsiminfo_name);

					nxprintf(f, "name", "%s", mcsiminfo_name);
					nxprintattr(f, "Format", mcformat && strlen(mcformat) ? mcformat : MCCODE_NAME);
					nxprintattr(f, "URL", "http://www.mccode.org");
					nxprintattr(f, "program", MCCODE_STRING);
					nxprintattr(f, "Instrument", mcinstrument_source);
					nxprintattr(f, "Trace", mcdotrace ? "yes" : "no");
					nxprintattr(f, "Gravitation", mcgravitation ? "yes" : "no");
					nxprintattr(f, "Seed", "%li", mcseed);
					nxprintattr(f, "Directory", mcdirname);
#ifdef USE_MPI
					if (mpi_node_count > 1)
						nxprintf(f, "Nodes", "%i", mpi_node_count);
#endif

					/* output parameter string ================================================ */
					if (NXmakegroup(f, "Param", "NXparameters") == NX_OK)
						if (NXopengroup(f, "Param", "NXparameters") == NX_OK) {
							int i;
							char string[CHAR_BUF_LENGTH];
							for (i = 0; i < mcnumipar; i++) {
								if (mcget_run_num() || (mcinputtable[i].val && strlen(mcinputtable[i].val))) {
									if (mcinputtable[i].par == NULL)
										strncpy(string, (mcinputtable[i].val ? mcinputtable[i].val : ""), CHAR_BUF_LENGTH);
									else
										(*mcinputtypes[mcinputtable[i].type].printer)(string, mcinputtable[i].par);

									nxprintf(f, mcinputtable[i].name, "%s", string);
									nxprintattr(f, mcinputtable[i].name, string);
								}
							}
							NXclosegroup(f); /* Param */
						} /* NXparameters */

					NXclosegroup(f); /* simulation */
				} /* NXsimulation */

				  /* create a group to hold all monitors */
			NXmakegroup(f, "data", "NXdetector");

			/* leave the NXentry opened (closed at exit) */
		} /* NXentry */
} /* mcinfo_out_nexus */

  /*******************************************************************************
  * mcdatainfo_out_nexus: output detector header
  *   mcdatainfo_out_nexus(detector) create group and write info to NeXus data file
  *   open data:NXdetector then filename:NXdata and write headers/attributes
  *   requires: NXentry to be opened
  *******************************************************************************/
static void
mcdatainfo_out_nexus(NXhandle f, MCDETECTOR detector)
{
	char data_name[32];
	if (!f || !detector.m || mcdisable_output_files) return;

	strcpy_valid(data_name,
		detector.filename && strlen(detector.filename) ?
		detector.filename : detector.component);

	/* the NXdetector group has been created in mcinfo_out_nexus (mcsiminfo_init) */
	if (NXopengroup(f, "data", "NXdetector") == NX_OK) {

		/* create and open the data group */
		/* this may fail when appending to list -> ignore/skip */
		NXMDisableErrorReporting(); /* unactivate NeXus error messages, as creation may fail */

		if (NXmakegroup(f, data_name, "NXdata") == NX_OK)
			if (NXopengroup(f, data_name, "NXdata") == NX_OK) {

				/* output metadata (as attributes) ======================================== */
				nxprintattr(f, "Date", detector.date);
				nxprintattr(f, "type", detector.type);
				nxprintattr(f, "Source", detector.instrument);
				nxprintattr(f, "component", detector.component);
				nxprintattr(f, "position", detector.position);

				nxprintattr(f, "title", detector.title);
				nxprintattr(f, !mcget_run_num() || mcget_run_num() >= mcget_ncount() ?
					"Ncount" :
					"ratio", detector.ncount);

				if (strlen(detector.filename)) {
					nxprintattr(f, "filename", detector.filename);
				}

				nxprintattr(f, "statistics", detector.statistics);
				nxprintattr(f, "signal", detector.signal);
				nxprintattr(f, "values", detector.values);

				if (detector.rank >= 1)
				{
					nxprintattr(f, "xvar", detector.xvar);
					nxprintattr(f, "yvar", detector.yvar);
					nxprintattr(f, "xlabel", detector.xlabel);
					nxprintattr(f, "ylabel", detector.ylabel);
					if (detector.rank > 1) {
						nxprintattr(f, "zvar", detector.zvar);
						nxprintattr(f, "zlabel", detector.zlabel);
					}
				}

				nxprintattr(f, abs(detector.rank) == 1 ?
					"xlimits" :
					"xylimits", detector.limits);
				nxprintattr(f, "variables",
					strcasestr(detector.format, "list") ? detector.ylabel : detector.variables);
				nxprintf(f, "distance", detector.position);
				nxprintf(f, "acquisition_mode",
					strcasestr(detector.format, "list") ? "event" : "summed");

				NXclosegroup(f);
			} /* NXdata (filename) */
		NXMEnableErrorReporting();  /* re-enable NeXus error messages */
		NXclosegroup(f);
	} /* NXdetector (data) */

} /* mcdatainfo_out_nexus */

  /*******************************************************************************
  * mcdetector_out_axis_nexus: write detector axis into current NXdata
  *   requires: NXdata to be opened
  *******************************************************************************/
int mcdetector_out_axis_nexus(NXhandle f, char *label, char *var, int rank, long length, double min, double max)
{
	if (!f || length <= 1 || mcdisable_output_files || max == min) return(NX_OK);
	else {
		double axis[length];
		char valid[32];
		int dim = (int)length;
		int i;
		int nprimary = 1;
		/* create an axis from [min:max] */
		for (i = 0; i < length; i++)
			axis[i] = min + (max - min)*(i + 0.5) / length;
		/* create the data set */
		strcpy_valid(valid, label);
		NXcompmakedata(f, valid, NX_FLOAT64, 1, &dim, NX_COMP_LZW, &dim);
		/* open it */
		if (NXopendata(f, valid) != NX_OK) {
			fprintf(stderr, "Warning: could not open axis rank %i '%s' (NeXus)\n",
				rank, valid);
			return(NX_ERROR);
		}
		/* put the axis and its attributes */
		NXputdata(f, axis);
		nxprintattr(f, "long_name", label);
		nxprintattr(f, "short_name", var);
		NXputattr(f, "axis", &rank, 1, NX_INT32);
		nxprintattr(f, "units", var);
		NXputattr(f, "primary", &nprimary, 1, NX_INT32);
		NXclosedata(f);

		return(NX_OK);
	}
} /* mcdetector_out_axis_nexus */

  /*******************************************************************************
  * mcdetector_out_array_nexus: write detector array into current NXdata (1D,2D)
  *   requires: NXdata to be opened
  *******************************************************************************/
int mcdetector_out_array_nexus(NXhandle f, char *part, double *data, MCDETECTOR detector)
{

	int dims[3] = { detector.m,detector.n,detector.p };  /* number of elements to write */
	int signal = 1;
	int exists = 0;
	int current_dims[3] = { 0,0,0 };
	int ret = NX_OK;

	if (!f || !data || !detector.m || mcdisable_output_files) return(NX_OK);

	/* when this is a list, we set 1st dimension to NX_UNLIMITED for creation */
	if (strcasestr(detector.format, "list")) dims[0] = NX_UNLIMITED;

	/* create the data set in NXdata group */
	NXMDisableErrorReporting(); /* unactivate NeXus error messages, as creation may fail */
								/* NXcompmakedata fails with NX_UNLIMITED */
	if (strcasestr(detector.format, "list"))
		ret = NXmakedata(f, part, NX_FLOAT64, detector.rank, dims);
	else
		ret = NXcompmakedata(f, part, NX_FLOAT64, detector.rank, dims, NX_COMP_LZW, dims);
	if (ret != NX_OK) {
		/* failed: data set already exists */
		int datatype = 0;
		int rank = 0;
		exists = 1;
		/* inquire current size of data set (nb of events stored) */
		NXopendata(f, part);
		NXgetinfo(f, &rank, current_dims, &datatype);
		NXclosedata(f);
	}
	NXMEnableErrorReporting();  /* re-enable NeXus error messages */
	dims[0] = detector.m; /* restore actual dimension from data writing */

						  /* open the data set */
	if (NXopendata(f, part) == NX_ERROR) {
		fprintf(stderr, "Warning: could not open DataSet %s '%s' (NeXus)\n",
			part, detector.title);
		return(NX_ERROR);
	}
	if (strcasestr(detector.format, "list")) {
		current_dims[1] = current_dims[2] = 0; /* set starting location for writing slab */
		NXputslab(f, data, current_dims, dims);
		if (!exists)
			printf("Events:   \"%s\"\n",
				strlen(detector.filename) ? detector.filename : detector.component);
	}
	else {
		NXputdata(f, data);
	}

	if (strstr(part, "data") || strstr(part, "events")) {
		NXputattr(f, "signal", &signal, 1, NX_INT32);
		nxprintattr(f, "short_name", detector.filename && strlen(detector.filename) ?
			detector.filename : detector.component);
	}
	nxprintattr(f, "long_name", "%s '%s'", part, detector.title);
	NXclosedata(f);

	return(NX_OK);
} /* mcdetector_out_array_nexus */

  /*******************************************************************************
  * mcdetector_out_data_nexus: write detector axes+data into current NXdata
  *   The data:NXdetector is opened, then filename:NXdata
  *   requires: NXentry to be opened
  *******************************************************************************/
int mcdetector_out_data_nexus(NXhandle f, MCDETECTOR detector)
{
	char data_name[32];

	if (!f || !detector.m || mcdisable_output_files) return(NX_OK);

	strcpy_valid(data_name,
		detector.filename && strlen(detector.filename) ?
		detector.filename : detector.component);

	/* the NXdetector group has been created in mcinfo_out_nexus (mcsiminfo_init) */
	if (NXopengroup(f, "data", "NXdetector") == NX_OK) {

		/* the NXdata group has been created in mcdatainfo_out_nexus */
		if (NXopengroup(f, data_name, "NXdata") == NX_OK) {

			/* write axes, for histogram data sets, not for lists */
			if (!strcasestr(detector.format, "list")) {
				mcdetector_out_axis_nexus(f, detector.xlabel, detector.xvar,
					1, detector.m, detector.xmin, detector.xmax);

				mcdetector_out_axis_nexus(f, detector.ylabel, detector.yvar,
					2, detector.n, detector.ymin, detector.ymax);

				mcdetector_out_axis_nexus(f, detector.zlabel, detector.zvar,
					3, detector.p, detector.zmin, detector.zmax);

			} /* !list */

			  /* write the actual data (appended if already exists) */
			if (!strcasestr(detector.format, "list")) {
				mcdetector_out_array_nexus(f, "data", detector.p1, detector);
				mcdetector_out_array_nexus(f, "errors", detector.p2, detector);
				mcdetector_out_array_nexus(f, "ncount", detector.p0, detector);
			}
			else
				mcdetector_out_array_nexus(f, "events", detector.p1, detector);

			NXclosegroup(f);
		} /* NXdata */
		NXclosegroup(f);
	} /* NXdetector */

	return(NX_OK);
} /* mcdetector_out_array_nexus */

#ifdef USE_MPI
  /*******************************************************************************
  * mcdetector_out_list_slaves: slaves send their list data to master which writes
  *   requires: NXentry to be opened
  * WARNING: this method has a flaw: it requires all nodes to flush the lists
  *   the same number of times. In case one node is just below the buffer size
  *   when finishing (e.g. monitor_nd), it may not trigger save but others may.
  *   Then the number of recv/send is not constant along nodes, and simulation stalls.
  *******************************************************************************/
MCDETECTOR mcdetector_out_list_slaves(MCDETECTOR detector)
{
	int     node_i = 0;

	if (mpi_node_rank != mpi_node_root) {
		/* MPI slave: slaves send their data to master: 2 MPI_Send calls */
		/* m, n, p must be sent first, since all slaves do not have the same number of events */
		int mnp[3] = { detector.m,detector.n,detector.p };

		if (mc_MPI_Send(mnp, 3, MPI_INT, mpi_node_root) != MPI_SUCCESS)
			fprintf(stderr, "Warning: proc %i to master: MPI_Send mnp list error (mcdetector_out_list_slaves)\n", mpi_node_rank);
		if (!detector.p1
			|| mc_MPI_Send(detector.p1, mnp[0] * mnp[1] * mnp[2], MPI_DOUBLE, mpi_node_root) != MPI_SUCCESS)
			fprintf(stderr, "Warning: proc %i to master: MPI_Send p1 list error: mnp=%i (mcdetector_out_list_slaves)\n", mpi_node_rank, abs(mnp[0] * mnp[1] * mnp[2]));
		/* slaves are done: sent mnp and p1 */
		return (detector);
	} /* end slaves */

	  /* MPI master: receive data from slaves sequentially: 2 MPI_Recv calls */
	for (node_i = 0; node_i<mpi_node_count; node_i++) {
		double *this_p1 = NULL;                               /* buffer to hold the list from slaves */
		int     mnp[3] = { 0,0,0 };  /* size of this buffer */
		if (node_i != mpi_node_root) { /* get data from slaves */
			if (mc_MPI_Recv(mnp, 3, MPI_INT, node_i) != MPI_SUCCESS)
				fprintf(stderr, "Warning: master from proc %i: "
					"MPI_Recv mnp list error (mcdetector_write_data)\n", node_i);
			if (mnp[0] * mnp[1] * mnp[2]) {
				this_p1 = (double *)calloc(mnp[0] * mnp[1] * mnp[2], sizeof(double));
				if (!this_p1 || mc_MPI_Recv(this_p1, abs(mnp[0] * mnp[1] * mnp[2]), MPI_DOUBLE, node_i) != MPI_SUCCESS)
					fprintf(stderr, "Warning: master from proc %i: "
						"MPI_Recv p1 list error: mnp=%i (mcdetector_write_data)\n", node_i, mnp[0] * mnp[1] * mnp[2]);
				else {
					detector.p1 = this_p1;
					detector.m = mnp[0]; detector.n = mnp[1]; detector.p = mnp[2];
					mcdetector_out_data_nexus(nxhandle, detector);
				}
			}
		} /* if not master */
	} /* for */

}
#endif

MCDETECTOR mcdetector_out_0D_nexus(MCDETECTOR detector)
{
	/* Write data set information to NeXus file. */
	MPI_MASTER(
		mcdatainfo_out_nexus(nxhandle, detector);
	);

	return(detector);
} /* mcdetector_out_0D_ascii */

MCDETECTOR mcdetector_out_1D_nexus(MCDETECTOR detector)
{
	MPI_MASTER(
		mcdatainfo_out_nexus(nxhandle, detector);
	mcdetector_out_data_nexus(nxhandle, detector);
	);
	return(detector);
} /* mcdetector_out_1D_ascii */

MCDETECTOR mcdetector_out_2D_nexus(MCDETECTOR detector)
{
	MPI_MASTER(
		mcdatainfo_out_nexus(nxhandle, detector);
	mcdetector_out_data_nexus(nxhandle, detector);
	);

#ifdef USE_MPI // and USE_NEXUS
	/* NeXus: slave nodes have master write their lists */
	if (strcasestr(detector.format, "list") && mpi_node_count > 1) {
		mcdetector_out_list_slaves(detector);
	}
#endif /* USE_MPI */

	return(detector);
} /* mcdetector_out_2D_nexus */

#endif /* USE_NEXUS*/








  /* ========================================================================== */

  /*                            Main input functions                            */
  /*            DETECTOR_OUT_xD function calls -> ascii or NeXus                */

  /* ========================================================================== */

  /*******************************************************************************
  * mcsiminfo_init:   open SIM and write header
  *******************************************************************************/
FILE *mcsiminfo_init(FILE *f)
{
	int exists = 0;
	int index;

	/* check format */
	if (!mcformat || !strlen(mcformat)
		|| !strcasecmp(mcformat, "MCSTAS") || !strcasecmp(mcformat, "MCXTRACE")
		|| !strcasecmp(mcformat, "PGPLOT") || !strcasecmp(mcformat, "GNUPLOT") || !strcasecmp(mcformat, "MCCODE")
		|| !strcasecmp(mcformat, "MATLAB")) {
		mcformat = "McCode";
#ifdef USE_NEXUS
	}
	else if (strcasestr(mcformat, "NeXus")) {
		/* Do nothing */
#endif
	}
	else {
		fprintf(stderr,
			"Warning: You have requested the output format %s which is unsupported by this binary. Resetting to standard %s format.\n", mcformat, "McCode");
		mcformat = "McCode";
	}

	/* open the SIM file if not defined yet */
	if (mcsiminfo_file || mcdisable_output_files)
		return (mcsiminfo_file);

#ifdef USE_NEXUS
	/* only master writes NeXus header: calls NXopen(nxhandle) */
	if (mcformat && strcasestr(mcformat, "NeXus")) {
		MPI_MASTER(
			mcsiminfo_file = mcnew_file(mcsiminfo_name, "h5", &exists);
		if (!mcsiminfo_file)
			fprintf(stderr,
				"Warning: could not open simulation description file '%s'\n",
				mcsiminfo_name);
		else
			mcinfo_out_nexus(nxhandle);
		);
		return(mcsiminfo_file); /* points to nxhandle */
	}
#endif

	/* write main description file (only MASTER) */
	MPI_MASTER(

		mcsiminfo_file = mcnew_file(mcsiminfo_name, "sim", &exists);
	if (!mcsiminfo_file)
		fprintf(stderr,
			"Warning: could not open simulation description file '%s'\n",
			mcsiminfo_name);
	else
	{
		/* write SIM header */
		time_t t = time(NULL);
		mcsiminfo_out("%s simulation description file for %s.\n",
			MCCODE_NAME, mcinstrument_name);
		mcsiminfo_out("Date:    %s", ctime(&t)); /* includes \n */
		mcsiminfo_out("Program: %s\n\n", MCCODE_STRING);

		mcsiminfo_out("begin instrument: %s\n", mcinstrument_name);
		mcinfo_out("  ", mcsiminfo_file);
		mcsiminfo_out("end instrument\n");

		mcsiminfo_out("\nbegin simulation: %s\n", mcdirname);
		mcruninfo_out("  ", mcsiminfo_file);
		mcsiminfo_out("end simulation\n");

	}
	return (mcsiminfo_file);

	); /* MPI_MASTER */

} /* mcsiminfo_init */

  /*******************************************************************************
  *   mcsiminfo_close:  close SIM
  *******************************************************************************/
void mcsiminfo_close()
{
	MPI_MASTER(
		if (mcsiminfo_file && !mcdisable_output_files) {
#ifdef USE_NEXUS
			if (mcformat && strcasestr(mcformat, "NeXus")) {
				time_t t = time(NULL);
				nxprintf(nxhandle, "end_time", ctime(&t));
				nxprintf(nxhandle, "duration", "%li", (long)t - mcstartdate);
				NXclosegroup(nxhandle); /* NXentry */
				NXclose(&nxhandle);
			}
			else
#endif
				fclose(mcsiminfo_file);
			);
	mcsiminfo_file = NULL;
		}
} /* mcsiminfo_close */

  /*******************************************************************************
  * mcdetector_out_0D: wrapper for 0D (single value).
  *   Output single detector/monitor data (p0, p1, p2).
  *   Title is t, component name is c.
  *******************************************************************************/
MCDETECTOR mcdetector_out_0D(char *t, double p0, double p1, double p2,
	char *c, Coords posa)
{
	/* import and perform basic detector analysis (and handle MPI reduce) */
	MCDETECTOR detector = mcdetector_import(mcformat,
		c, (t ? t : MCCODE_STRING " data"),
		1, 1, 1,
		"I", "", "",
		"I", "", "",
		0, 0, 0, 0, 0, 0, "",
		&p0, &p1, &p2, posa); /* write Detector: line */

#ifdef USE_NEXUS
	if (strcasestr(detector.format, "NeXus"))
		return(mcdetector_out_0D_nexus(detector));
	else
#endif
		return(mcdetector_out_0D_ascii(detector));

} /* mcdetector_out_0D */



  /*******************************************************************************
  * mcdetector_out_1D: wrapper for 1D.
  *   Output 1d detector data (p0, p1, p2) for n bins linearly
  *   distributed across the range x1..x2 (x1 is lower limit of first
  *   bin, x2 is upper limit of last bin). Title is t, axis labels are xl
  *   and yl. File name is f, component name is c.
  *******************************************************************************/
MCDETECTOR mcdetector_out_1D(char *t, char *xl, char *yl,
	char *xvar, double x1, double x2,
	long n,
	double *p0, double *p1, double *p2, char *f,
	char *c, Coords posa)
{

	/* import and perform basic detector analysis (and handle MPI_Reduce) */
	MCDETECTOR detector = mcdetector_import(mcformat,
		c, (t ? t : MCCODE_STRING " 1D data"),
		n, 1, 1,
		xl, yl, (n > 1 ? "Signal per bin" : " Signal"),
		xvar, "(I,I_err)", "I",
		x1, x2, 0, 0, 0, 0, f,
		p0, p1, p2, posa); /* write Detector: line */
	if (!detector.p1 || !detector.m) return(detector);

#ifdef USE_NEXUS
	if (strcasestr(detector.format, "NeXus"))
		return(mcdetector_out_1D_nexus(detector));
	else
#endif
		return(mcdetector_out_1D_ascii(detector));

} /* mcdetector_out_1D */

  /*******************************************************************************
  * mcdetector_out_2D: wrapper for 2D.
  *   special case for list: master creates file first, then slaves append their blocks without header
  *******************************************************************************/
MCDETECTOR mcdetector_out_2D(char *t, char *xl, char *yl,
	double x1, double x2, double y1, double y2,
	long m, long n,
	double *p0, double *p1, double *p2, char *f,
	char *c, Coords posa)
{
	char xvar[CHAR_BUF_LENGTH];
	char yvar[CHAR_BUF_LENGTH];

	/* create short axes labels */
	if (xl && strlen(xl)) { strncpy(xvar, xl, CHAR_BUF_LENGTH); xvar[2] = '\0'; }
	else strcpy(xvar, "x");
	if (yl && strlen(yl)) { strncpy(yvar, yl, CHAR_BUF_LENGTH); yvar[2] = '\0'; }
	else strcpy(yvar, "y");

	MCDETECTOR detector;

	/* import and perform basic detector analysis (and handle MPI_Reduce) */
	if (abs(m) == 1) {// n>1 on Y, m==1 on X: 1D, no X axis
		detector = mcdetector_import(mcformat,
			c, (t ? t : MCCODE_STRING " 1D data"),
			m, n, 1,
			yl, xl, "Signal per bin",
			yvar, xvar, "I",
			y1, y2, x1, x1, 0, 0, f,
			p0, p1, p2, posa); /* write Detector: line */
	}
	else {
		detector = mcdetector_import(mcformat,
			c, (t ? t : MCCODE_STRING " 2D data"),
			m, n, 1,
			xl, yl, "Signal per bin",
			xvar, yvar, "I",
			x1, x2, y1, y2, 0, 0, f,
			p0, p1, p2, posa); /* write Detector: line */
	}

	if (!detector.p1 || !detector.m) return(detector);

#ifdef USE_NEXUS
	if (strcasestr(detector.format, "NeXus"))
		return(mcdetector_out_2D_nexus(detector));
	else
#endif
		return(mcdetector_out_2D_ascii(detector));

} /* mcdetector_out_2D */

  /*******************************************************************************
  * mcdetector_out_list: wrapper for list output (calls out_2D with mcformat+"list").
  *   m=number of events, n=size of each event
  *******************************************************************************/
MCDETECTOR mcdetector_out_list(char *t, char *xl, char *yl,
	long m, long n,
	double *p1, char *f,
	char *c, Coords posa)
{
	char       format_new[CHAR_BUF_LENGTH];
	char      *format_org;
	MCDETECTOR detector;

	format_org = mcformat;
	strcpy(format_new, mcformat);
	strcat(format_new, " list");
	mcformat = format_new;

	detector = mcdetector_out_2D(t, xl, yl,
		1, abs(m), 1, abs(n),
		m, n,
		NULL, p1, NULL, f,
		c, posa);

	mcformat = format_org;
	return(detector);
}

/*******************************************************************************
* mcuse_dir: set data/sim storage directory and create it,
* or exit with error if exists
******************************************************************************/
static void
mcuse_dir(char *dir)
{
	if (!dir || !strlen(dir)) return;
#ifdef MC_PORTABLE
	fprintf(stderr, "Error: "
		"Directory output cannot be used with portable simulation (mcuse_dir)\n");
	exit(1);
#else  /* !MC_PORTABLE */
	/* handle file://directory URL type */
	if (strncmp(dir, "file://", strlen("file://")))
		mcdirname = dir;
	else
		mcdirname = dir + strlen("file://");



	MPI_MASTER(
		if (mkdir(mcdirname, 0777)) {
#ifndef DANSE
			fprintf(stderr, "Error: unable to create directory '%s' (mcuse_dir)\n", dir);
			fprintf(stderr, "(Maybe the directory already exists?)\n");
#endif
#ifdef USE_MPI
			MPI_Abort(MPI_COMM_WORLD, -1);
#endif
			exit(-1);
		}
	); /* MPI_MASTER */

	   /* remove trailing PATHSEP (if any) */
	while (strlen(mcdirname) && mcdirname[strlen(mcdirname) - 1] == MC_PATHSEP_C)
		mcdirname[strlen(mcdirname) - 1] = '\0';
#endif /* !MC_PORTABLE */
} /* mcuse_dir */

  /*******************************************************************************
  * mcinfo: display instrument simulation info to stdout and exit
  *******************************************************************************/
static void
mcinfo(void)
{
	fprintf(stdout, "begin instrument: %s\n", mcinstrument_name);
	mcinfo_out("  ", stdout);
	fprintf(stdout, "end instrument\n");
	fprintf(stdout, "begin simulation: %s\n", mcdirname ? mcdirname : ".");
	mcruninfo_out("  ", stdout);
	fprintf(stdout, "end simulation\n");
	exit(0); /* includes MPI_Finalize in MPI mode */
} /* mcinfo */

#endif /* ndef MCCODE_R_IO_C */

  /* end of the I/O section =================================================== */







  /*******************************************************************************
  * mcset_ncount: set total number of rays to generate
  *******************************************************************************/
void mcset_ncount(unsigned long long int count)
{
	mcncount = count;
}

/* mcget_ncount: get total number of rays to generate */
unsigned long long int mcget_ncount(void)
{
	return mcncount;
}

/* mcget_run_num: get curent number of rays in TRACE */
unsigned long long int mcget_run_num(void)
{
	return mcrun_num;
}

/* mcsetn_arg: get ncount from a string argument */
static void
mcsetn_arg(char *arg)
{
	mcset_ncount((long long int) strtod(arg, NULL));
}

/* mcsetseed: set the random generator seed from a string argument */
static void
mcsetseed(char *arg)
{
	mcseed = atol(arg);
	if (mcseed) {
		srandom(mcseed);
	}
	else {
		fprintf(stderr, "Error: seed must not be zero (mcsetseed)\n");
		exit(1);
	}
}

/* Following part is only embedded when not redundent with mccode-r.h ========= */

#ifndef MCCODE_H

/* SECTION: MCDISPLAY support. =============================================== */

/*******************************************************************************
* Just output MCDISPLAY keywords to be caught by an external plotter client.
*******************************************************************************/

void mcdis_magnify(char *what) {
	printf("MCDISPLAY: magnify('%s')\n", what);
}

void mcdis_line(double x1, double y1, double z1,
	double x2, double y2, double z2) {
	printf("MCDISPLAY: multiline(2,%g,%g,%g,%g,%g,%g)\n",
		x1, y1, z1, x2, y2, z2);
}

void mcdis_dashed_line(double x1, double y1, double z1,
	double x2, double y2, double z2, int n) {
	int i;
	const double dx = (x2 - x1) / (2 * n + 1);
	const double dy = (y2 - y1) / (2 * n + 1);
	const double dz = (z2 - z1) / (2 * n + 1);

	for (i = 0; i < n + 1; i++)
		mcdis_line(x1 + 2 * i*dx, y1 + 2 * i*dy, z1 + 2 * i*dz,
			x1 + (2 * i + 1)*dx, y1 + (2 * i + 1)*dy, z1 + (2 * i + 1)*dz);
}

void mcdis_multiline(int count, ...) {
	va_list ap;
	double x, y, z;

	printf("MCDISPLAY: multiline(%d", count);
	va_start(ap, count);
	while (count--)
	{
		x = va_arg(ap, double);
		y = va_arg(ap, double);
		z = va_arg(ap, double);
		printf(",%g,%g,%g", x, y, z);
	}
	va_end(ap);
	printf(")\n");
}

void mcdis_rectangle(char* plane, double x, double y, double z,
	double width, double height) {
	/* draws a rectangle in the plane           */
	/* x is ALWAYS width and y is ALWAYS height */
	if (strcmp("xy", plane) == 0) {
		mcdis_multiline(5,
			x - width / 2, y - height / 2, z,
			x + width / 2, y - height / 2, z,
			x + width / 2, y + height / 2, z,
			x - width / 2, y + height / 2, z,
			x - width / 2, y - height / 2, z);
	}
	else if (strcmp("xz", plane) == 0) {
		mcdis_multiline(5,
			x - width / 2, y, z - height / 2,
			x + width / 2, y, z - height / 2,
			x + width / 2, y, z + height / 2,
			x - width / 2, y, z + height / 2,
			x - width / 2, y, z - height / 2);
	}
	else if (strcmp("yz", plane) == 0) {
		mcdis_multiline(5,
			x, y - height / 2, z - width / 2,
			x, y - height / 2, z + width / 2,
			x, y + height / 2, z + width / 2,
			x, y + height / 2, z - width / 2,
			x, y - height / 2, z - width / 2);
	}
	else {

		fprintf(stderr, "Error: Definition of plane %s unknown\n", plane);
		exit(1);
	}
}

/*  draws a box with center at (x, y, z) and
width (deltax), height (deltay), length (deltaz) */
void mcdis_box(double x, double y, double z,
	double width, double height, double length) {

	mcdis_rectangle("xy", x, y, z - length / 2, width, height);
	mcdis_rectangle("xy", x, y, z + length / 2, width, height);
	mcdis_line(x - width / 2, y - height / 2, z - length / 2,
		x - width / 2, y - height / 2, z + length / 2);
	mcdis_line(x - width / 2, y + height / 2, z - length / 2,
		x - width / 2, y + height / 2, z + length / 2);
	mcdis_line(x + width / 2, y - height / 2, z - length / 2,
		x + width / 2, y - height / 2, z + length / 2);
	mcdis_line(x + width / 2, y + height / 2, z - length / 2,
		x + width / 2, y + height / 2, z + length / 2);
}

void mcdis_circle(char *plane, double x, double y, double z, double r) {
	printf("MCDISPLAY: circle('%s',%g,%g,%g,%g)\n", plane, x, y, z, r);
}

/* SECTION: coordinates handling ============================================ */

/*******************************************************************************
* Since we use a lot of geometric calculations using Cartesian coordinates,
* we collect some useful routines here. However, it is also permissible to
* work directly on the underlying struct coords whenever that is most
* convenient (that is, the type Coords is not abstract).
*
* Coordinates are also used to store rotation angles around x/y/z axis.
*
* Since coordinates are used much like a basic type (such as double), the
* structure itself is passed and returned, rather than a pointer.
*
* At compile-time, the values of the coordinates may be unknown (for example
* a motor position). Hence coordinates are general expressions and not simple
* numbers. For this we used the type Coords_exp which has three CExp
* fields. For runtime (or calculations possible at compile time), we use
* Coords which contains three double fields.
*******************************************************************************/

/* coords_set: Assign coordinates. */
Coords
coords_set(MCNUM x, MCNUM y, MCNUM z)
{
	Coords a;

	a.x = x;
	a.y = y;
	a.z = z;
	return a;
}

/* coords_get: get coordinates. Required when 'x','y','z' are #defined as ray pars */
Coords
coords_get(Coords a, MCNUM *x, MCNUM *y, MCNUM *z)
{
	*x = a.x;
	*y = a.y;
	*z = a.z;
	return a;
}

/* coords_add: Add two coordinates. */
Coords
coords_add(Coords a, Coords b)
{
	Coords c;

	c.x = a.x + b.x;
	c.y = a.y + b.y;
	c.z = a.z + b.z;
	if (fabs(c.z) < 1e-14) c.z = 0.0;
	return c;
}

/* coords_sub: Subtract two coordinates. */
Coords
coords_sub(Coords a, Coords b)
{
	Coords c;

	c.x = a.x - b.x;
	c.y = a.y - b.y;
	c.z = a.z - b.z;
	if (fabs(c.z) < 1e-14) c.z = 0.0;
	return c;
}

/* coords_neg: Negate coordinates. */
Coords
coords_neg(Coords a)
{
	Coords b;

	b.x = -a.x;
	b.y = -a.y;
	b.z = -a.z;
	return b;
}

/* coords_scale: Scale a vector. */
Coords coords_scale(Coords b, double scale) {
	Coords a;

	a.x = b.x*scale;
	a.y = b.y*scale;
	a.z = b.z*scale;
	return a;
}

/* coords_sp: Scalar product: a . b */
double coords_sp(Coords a, Coords b) {
	double value;

	value = a.x*b.x + a.y*b.y + a.z*b.z;
	return value;
}

/* coords_xp: Cross product: a = b x c. */
Coords coords_xp(Coords b, Coords c) {
	Coords a;

	a.x = b.y*c.z - c.y*b.z;
	a.y = b.z*c.x - c.z*b.x;
	a.z = b.x*c.y - c.x*b.y;
	return a;
}

/* coords_mirror: Mirror a in plane (through the origin) defined by normal n*/
Coords coords_mirror(Coords a, Coords n) {
	double t = scalar_prod(n.x, n.y, n.z, n.x, n.y, n.z);
	Coords b;
	if (t != 1) {
		t = sqrt(t);
		n.x /= t;
		n.y /= t;
		n.z /= t;
	}
	t = scalar_prod(a.x, a.y, a.z, n.x, n.y, n.z);
	b.x = a.x - 2 * t*n.x;
	b.y = a.y - 2 * t*n.y;
	b.z = a.z - 2 * t*n.z;
	return b;
}

/* coords_print: Print out vector values. */
void coords_print(Coords a) {

	fprintf(stdout, "(%f, %f, %f)\n", a.x, a.y, a.z);
	return;
}

mcstatic inline void coords_norm(Coords* c) {
	double temp = coords_sp(*c, *c);

	// Skip if we will end dividing by zero
	if (temp == 0) return;

	temp = sqrt(temp);

	c->x /= temp;
	c->y /= temp;
	c->z /= temp;
}

/*******************************************************************************
* The Rotation type implements a rotation transformation of a coordinate
* system in the form of a double[3][3] matrix.
*
* Contrary to the Coords type in coords.c, rotations are passed by
* reference. Functions that yield new rotations do so by writing to an
* explicit result parameter; rotations are not returned from functions. The
* reason for this is that arrays cannot by returned from functions (though
* structures can; thus an alternative would have been to wrap the
* double[3][3] array up in a struct). Such are the ways of C programming.
*
* A rotation represents the tranformation of the coordinates of a vector when
* changing between coordinate systems that are rotated with respect to each
* other. For example, suppose that coordinate system Q is rotated 45 degrees
* around the Z axis with respect to coordinate system P. Let T be the
* rotation transformation representing a 45 degree rotation around Z. Then to
* get the coordinates of a vector r in system Q, apply T to the coordinates
* of r in P. If r=(1,0,0) in P, it will be (sqrt(1/2),-sqrt(1/2),0) in
* Q. Thus we should be careful when interpreting the sign of rotation angles:
* they represent the rotation of the coordinate systems, not of the
* coordinates (which has opposite sign).
*******************************************************************************/

/*******************************************************************************
* rot_set_rotation: Get transformation for rotation first phx around x axis,
* then phy around y, then phz around z.
*******************************************************************************/
void
rot_set_rotation(Rotation t, double phx, double phy, double phz)
{
	if ((phx == 0) && (phy == 0) && (phz == 0)) {
		t[0][0] = 1.0;
		t[0][1] = 0.0;
		t[0][2] = 0.0;
		t[1][0] = 0.0;
		t[1][1] = 1.0;
		t[1][2] = 0.0;
		t[2][0] = 0.0;
		t[2][1] = 0.0;
		t[2][2] = 1.0;
	}
	else {
		double cx = cos(phx);
		double sx = sin(phx);
		double cy = cos(phy);
		double sy = sin(phy);
		double cz = cos(phz);
		double sz = sin(phz);

		t[0][0] = cy*cz;
		t[0][1] = sx*sy*cz + cx*sz;
		t[0][2] = sx*sz - cx*sy*cz;
		t[1][0] = -cy*sz;
		t[1][1] = cx*cz - sx*sy*sz;
		t[1][2] = sx*cz + cx*sy*sz;
		t[2][0] = sy;
		t[2][1] = -sx*cy;
		t[2][2] = cx*cy;
	}
}

/*******************************************************************************
* rot_test_identity: Test if rotation is identity
*******************************************************************************/
int
rot_test_identity(Rotation t)
{
	return (t[0][0] + t[1][1] + t[2][2] == 3);
}

/*******************************************************************************
* rot_mul: Matrix multiplication of transformations (this corresponds to
* combining transformations). After rot_mul(T1, T2, T3), doing T3 is
* equal to doing first T2, then T1.
* Note that T3 must not alias (use the same array as) T1 or T2.
*******************************************************************************/
void
rot_mul(Rotation t1, Rotation t2, Rotation t3)
{
	if (rot_test_identity(t1)) {
		rot_copy(t3, t2);
	}
	else if (rot_test_identity(t2)) {
		rot_copy(t3, t1);
	}
	else {
		int i, j;
		for (i = 0; i < 3; i++)
			for (j = 0; j < 3; j++)
				t3[i][j] = t1[i][0] * t2[0][j] + t1[i][1] * t2[1][j] + t1[i][2] * t2[2][j];
	}
}

/*******************************************************************************
* rot_copy: Copy a rotation transformation (arrays cannot be assigned in C).
*******************************************************************************/
void
rot_copy(Rotation dest, Rotation src)
{
	int i, j;
	for (i = 0; i < 3; i++)
		for (j = 0; j < 3; j++)
			dest[i][j] = src[i][j];
}

/*******************************************************************************
* rot_transpose: Matrix transposition, which is inversion for Rotation matrices
*******************************************************************************/
void
rot_transpose(Rotation src, Rotation dst)
{
	dst[0][0] = src[0][0];
	dst[0][1] = src[1][0];
	dst[0][2] = src[2][0];
	dst[1][0] = src[0][1];
	dst[1][1] = src[1][1];
	dst[1][2] = src[2][1];
	dst[2][0] = src[0][2];
	dst[2][1] = src[1][2];
	dst[2][2] = src[2][2];
}

/*******************************************************************************
* rot_apply: returns t*a
*******************************************************************************/
Coords
rot_apply(Rotation t, Coords a)
{
	Coords b;
	if (rot_test_identity(t)) {
		return a;
	}
	else {
		b.x = t[0][0] * a.x + t[0][1] * a.y + t[0][2] * a.z;
		b.y = t[1][0] * a.x + t[1][1] * a.y + t[1][2] * a.z;
		b.z = t[2][0] * a.x + t[2][1] * a.y + t[2][2] * a.z;
		return b;
	}
}

/**
* Pretty-printing of rotation matrices.
*/
void rot_print(Rotation rot) {
	printf("[ %4.2f %4.2f %4.2f ]\n",
		rot[0][0], rot[0][1], rot[0][2]);
	printf("[ %4.2f %4.2f %4.2f ]\n",
		rot[1][0], rot[1][1], rot[1][2]);
	printf("[ %4.2f %4.2f %4.2f ]\n\n",
		rot[2][0], rot[2][1], rot[2][2]);
}

/**
* Vector product: used by vec_prod (mccode-r.h). Use coords_xp for Coords.
*/
mcstatic inline void vec_prod_func(double *x, double *y, double *z,
	double x1, double y1, double z1,
	double x2, double y2, double z2) {
	*x = (y1)*(z2)-(y2)*(z1);
	*y = (z1)*(x2)-(z2)*(x1);
	*z = (x1)*(y2)-(x2)*(y1);
}

/**
* Scalar product: use coords_sp for Coords.
*/
mcstatic inline double scalar_prod(
	double x1, double y1, double z1,
	double x2, double y2, double z2) {
	return ((x1 * x2) + (y1 * y2) + (z1 * z2));
}

/*******************************************************************************
* mccoordschange: applies rotation to (x y z) and (vx vy vz) and Spin (sx,sy,sz)
*******************************************************************************/
void
mccoordschange(Coords a, Rotation t, double *x, double *y, double *z,
	double *vx, double *vy, double *vz, double *sx, double *sy, double *sz)
{
	Coords b, c;

	b.x = *x;
	b.y = *y;
	b.z = *z;
	c = rot_apply(t, b);
	b = coords_add(c, a);
	*x = b.x;
	*y = b.y;
	*z = b.z;

	if (*vz != 0.0 || *vx != 0.0 || *vy != 0.0) mccoordschange_polarisation(t, vx, vy, vz);

	if (*sz != 0.0 || *sx != 0.0 || *sy != 0.0) mccoordschange_polarisation(t, sx, sy, sz);

}

/*******************************************************************************
* mccoordschange_polarisation: applies rotation to vector (sx sy sz)
*******************************************************************************/
void
mccoordschange_polarisation(Rotation t, double *sx, double *sy, double *sz)
{
	Coords b, c;

	b.x = *sx;
	b.y = *sy;
	b.z = *sz;
	c = rot_apply(t, b);
	*sx = c.x;
	*sy = c.y;
	*sz = c.z;
}

/* SECTION: vector math  ==================================================== */

/* normal_vec_func: Compute normal vector to (x,y,z). */
mcstatic inline void normal_vec_func(double *nx, double *ny, double *nz,
	double x, double y, double z)
{
	double ax = fabs(x);
	double ay = fabs(y);
	double az = fabs(z);
	double l;
	if (x == 0 && y == 0 && z == 0)
	{
		*nx = 0;
		*ny = 0;
		*nz = 0;
		return;
	}
	if (ax < ay)
	{
		if (ax < az)
		{                           /* Use X axis */
			l = sqrt(z*z + y*y);
			*nx = 0;
			*ny = z / l;
			*nz = -y / l;
			return;
		}
	}
	else
	{
		if (ay < az)
		{                           /* Use Y axis */
			l = sqrt(z*z + x*x);
			*nx = z / l;
			*ny = 0;
			*nz = -x / l;
			return;
		}
	}
	/* Use Z axis */
	l = sqrt(y*y + x*x);
	*nx = y / l;
	*ny = -x / l;
	*nz = 0;
} /* normal_vec */

  /*******************************************************************************
  * solve_2nd_order: second order equation solve: A*t^2 + B*t + C = 0
  * solve_2nd_order(&t1, NULL, A,B,C)
  *   returns 0 if no solution was found, or set 't1' to the smallest positive
  *   solution.
  * solve_2nd_order(&t1, &t2, A,B,C)
  *   same as with &t2=NULL, but also returns the second solution.
  * EXAMPLE usage for intersection of a trajectory with a plane in gravitation
  * field (gx,gy,gz):
  * The neutron starts at point r=(x,y,z) with velocityv=(vx vy vz). The plane
  * has a normal vector n=(nx,ny,nz) and contains the point W=(wx,wy,wz).
  * The problem consists in solving the 2nd order equation:
  *      1/2.n.g.t^2 + n.v.t + n.(r-W) = 0
  * so that A = 0.5 n.g; B = n.v; C = n.(r-W);
  * Without acceleration, t=-n.(r-W)/n.v
  ******************************************************************************/
int solve_2nd_order(double *t1, double *t2,
	double A, double B, double C)
{
	int ret = 0;

	if (!t1) return 0;
	*t1 = 0;
	if (t2) *t2 = 0;

	if (fabs(A) < 1E-10) /* approximate to linear equation: A ~ 0 */
	{
		if (B) { *t1 = -C / B; ret = 1; if (t2) *t2 = *t1; }
		/* else no intersection: A=B=0 ret=0 */
	}
	else
	{
		double D;
		D = B*B - 4 * A*C;
		if (D >= 0) /* Delta > 0: two solutions */
		{
			double sD, dt1, dt2;
			sD = sqrt(D);
			dt1 = (-B + sD) / 2 / A;
			dt2 = (-B - sD) / 2 / A;
			/* we identify very small values with zero */
			if (fabs(dt1) < 1e-10) dt1 = 0.0;
			if (fabs(dt2) < 1e-10) dt2 = 0.0;

			/* now we choose the smallest positive solution */
			if (dt1 <= 0.0 && dt2>0.0) ret = 2; /* dt2 positive */
			else if (dt2 <= 0.0 && dt1>0.0) ret = 1; /* dt1 positive */
			else if (dt1> 0.0 && dt2>0.0)
			{
				if (dt1 < dt2) ret = 1; else ret = 2;
			} /* all positive: min(dt1,dt2) */
			  /* else two solutions are negative. ret=-1 */
			if (ret == 1) { *t1 = dt1;  if (t2) *t2 = dt2; }
			else { *t1 = dt2;  if (t2) *t2 = dt1; }
			ret = 2;  /* found 2 solutions and t1 is the positive one */
		} /* else Delta <0: no intersection. ret=0 */
	}
	return(ret);
} /* solve_2nd_order */

  /*******************************************************************************
  * randvec_target_circle: Choose random direction towards target at (x,y,z)
  * with given radius.
  * If radius is zero, choose random direction in full 4PI, no target.
  ******************************************************************************/
void
randvec_target_circle(double *xo, double *yo, double *zo, double *solid_angle,
	double xi, double yi, double zi, double radius)
{
	double l2, phi, theta, nx, ny, nz, xt, yt, zt, xu, yu, zu;

	if (radius == 0.0)
	{
		/* No target, choose uniformly a direction in full 4PI solid angle. */
		theta = acos(1 - rand0max(2));
		phi = rand0max(2 * PI);
		if (solid_angle)
			*solid_angle = 4 * PI;
		nx = 1;
		ny = 0;
		nz = 0;
		yi = sqrt(xi*xi + yi*yi + zi*zi);
		zi = 0;
		xi = 0;
	}
	else
	{
		double costheta0;
		l2 = xi*xi + yi*yi + zi*zi; /* sqr Distance to target. */
		costheta0 = sqrt(l2 / (radius*radius + l2));
		if (radius < 0) costheta0 *= -1;
		if (solid_angle)
		{
			/* Compute solid angle of target as seen from origin. */
			*solid_angle = 2 * PI*(1 - costheta0);
		}

		/* Now choose point uniformly on circle surface within angle theta0 */
		theta = acos(1 - rand0max(1 - costheta0)); /* radius on circle */
		phi = rand0max(2 * PI); /* rotation on circle at given radius */
								/* Now, to obtain the desired vector rotate (xi,yi,zi) angle theta around a
								perpendicular axis u=i x n and then angle phi around i. */
		if (xi == 0 && zi == 0)
		{
			nx = 1;
			ny = 0;
			nz = 0;
		}
		else
		{
			nx = -zi;
			nz = xi;
			ny = 0;
		}
	}

	/* [xyz]u = [xyz]i x n[xyz] (usually vertical) */
	vec_prod(xu, yu, zu, xi, yi, zi, nx, ny, nz);
	/* [xyz]t = [xyz]i rotated theta around [xyz]u */
	rotate(xt, yt, zt, xi, yi, zi, theta, xu, yu, zu);
	/* [xyz]o = [xyz]t rotated phi around n[xyz] */
	rotate(*xo, *yo, *zo, xt, yt, zt, phi, xi, yi, zi);
} /* randvec_target_circle */

  /*******************************************************************************
  * randvec_target_rect_angular: Choose random direction towards target at
  * (xi,yi,zi) with given ANGULAR dimension height x width. height=phi_x=[0,PI],
  * width=phi_y=[0,2*PI] (radians)
  * If height or width is zero, choose random direction in full 4PI, no target.
  *******************************************************************************/
void
randvec_target_rect_angular(double *xo, double *yo, double *zo, double *solid_angle,
	double xi, double yi, double zi, double width, double height, Rotation A)
{
	double theta, phi, nx, ny, nz, xt, yt, zt, xu, yu, zu;
	Coords tmp;
	Rotation Ainverse;

	rot_transpose(A, Ainverse);

	if (height == 0.0 || width == 0.0)
	{
		randvec_target_circle(xo, yo, zo, solid_angle,
			xi, yi, zi, 0);
		return;
	}
	else
	{
		if (solid_angle)
		{
			/* Compute solid angle of target as seen from origin. */
			*solid_angle = 2 * fabs(width*sin(height / 2));
		}

		/* Go to global coordinate system */

		tmp = coords_set(xi, yi, zi);
		tmp = rot_apply(Ainverse, tmp);
		coords_get(tmp, &xi, &yi, &zi);

		/* Now choose point uniformly on the unit sphere segment with angle theta/phi */
		phi = width*randpm1() / 2.0;
		theta = asin(randpm1()*sin(height / 2.0));
		/* Now, to obtain the desired vector rotate (xi,yi,zi) angle theta around
		n, and then phi around u. */
		if (xi == 0 && zi == 0)
		{
			nx = 1;
			ny = 0;
			nz = 0;
		}
		else
		{
			nx = -zi;
			nz = xi;
			ny = 0;
		}
	}

	/* [xyz]u = [xyz]i x n[xyz] (usually vertical) */
	vec_prod(xu, yu, zu, xi, yi, zi, nx, ny, nz);
	/* [xyz]t = [xyz]i rotated theta around [xyz]u */
	rotate(xt, yt, zt, xi, yi, zi, theta, nx, ny, nz);
	/* [xyz]o = [xyz]t rotated phi around n[xyz] */
	rotate(*xo, *yo, *zo, xt, yt, zt, phi, xu, yu, zu);

	/* Go back to local coordinate system */
	tmp = coords_set(*xo, *yo, *zo);
	tmp = rot_apply(A, tmp);
	coords_get(tmp, &*xo, &*yo, &*zo);

} /* randvec_target_rect_angular */

  /*******************************************************************************
  * randvec_target_rect_real: Choose random direction towards target at (xi,yi,zi)
  * with given dimension height x width (in meters !).
  *
  * Local emission coordinate is taken into account and corrected for 'order' times.
  * (See remarks posted to mcstas-users by George Apostolopoulus <gapost@ipta.demokritos.gr>)
  *
  * If height or width is zero, choose random direction in full 4PI, no target.
  *
  * Traditionally, this routine had the name randvec_target_rect - this is now a
  * a define (see mcstas-r.h) pointing here. If you use the old rouine, you are NOT
  * taking the local emmission coordinate into account.
  *******************************************************************************/

void
randvec_target_rect_real(double *xo, double *yo, double *zo, double *solid_angle,
	double xi, double yi, double zi,
	double width, double height, Rotation A,
	double lx, double ly, double lz, int order)
{
	double dx, dy, dist, dist_p, nx, ny, nz, mx, my, mz, n_norm, m_norm;
	double cos_theta;
	Coords tmp;
	Rotation Ainverse;

	rot_transpose(A, Ainverse);

	if (height == 0.0 || width == 0.0)
	{
		randvec_target_circle(xo, yo, zo, solid_angle,
			xi, yi, zi, 0);
		return;
	}
	else
	{

		/* Now choose point uniformly on rectangle within width x height */
		dx = width*randpm1() / 2.0;
		dy = height*randpm1() / 2.0;

		/* Determine distance to target plane*/
		dist = sqrt(xi*xi + yi*yi + zi*zi);
		/* Go to global coordinate system */

		tmp = coords_set(xi, yi, zi);
		tmp = rot_apply(Ainverse, tmp);
		coords_get(tmp, &xi, &yi, &zi);

		/* Determine vector normal to trajectory axis (z) and gravity [0 1 0] */
		vec_prod(nx, ny, nz, xi, yi, zi, 0, 1, 0);

		/* This now defines the x-axis, normalize: */
		n_norm = sqrt(nx*nx + ny*ny + nz*nz);
		nx = nx / n_norm;
		ny = ny / n_norm;
		nz = nz / n_norm;

		/* Now, determine our y-axis (vertical in many cases...) */
		vec_prod(mx, my, mz, xi, yi, zi, nx, ny, nz);
		m_norm = sqrt(mx*mx + my*my + mz*mz);
		mx = mx / m_norm;
		my = my / m_norm;
		mz = mz / m_norm;

		/* Our output, random vector can now be defined by linear combination: */

		*xo = xi + dx * nx + dy * mx;
		*yo = yi + dx * ny + dy * my;
		*zo = zi + dx * nz + dy * mz;

		/* Go back to local coordinate system */
		tmp = coords_set(*xo, *yo, *zo);
		tmp = rot_apply(A, tmp);
		coords_get(tmp, &*xo, &*yo, &*zo);

		/* Go back to local coordinate system */
		tmp = coords_set(xi, yi, zi);
		tmp = rot_apply(A, tmp);
		coords_get(tmp, &xi, &yi, &zi);

		if (solid_angle) {
			/* Calculate vector from local point to remote random point */
			lx = *xo - lx;
			ly = *yo - ly;
			lz = *zo - lz;
			dist_p = sqrt(lx*lx + ly*ly + lz*lz);

			/* Adjust the 'solid angle' */
			/* 1/r^2 to the chosen point times cos(\theta) between the normal */
			/* vector of the target rectangle and direction vector of the chosen point. */
			cos_theta = (xi * lx + yi * ly + zi * lz) / (dist * dist_p);
			*solid_angle = width * height / (dist_p * dist_p);
			int counter;
			for (counter = 0; counter < order; counter++) {
				*solid_angle = *solid_angle * cos_theta;
			}
		}
	}
} /* randvec_target_rect_real */

  /* SECTION: random numbers ================================================== */

  /*
  * Copyright (c) 1983 Regents of the University of California.
  * All rights reserved.
  *
  * Redistribution and use in source and binary forms are permitted
  * provided that the above copyright notice and this paragraph are
  * duplicated in all such forms and that any documentation,
  * advertising materials, and other materials related to such
  * distribution and use acknowledge that the software was developed
  * by the University of California, Berkeley.  The name of the
  * University may not be used to endorse or promote products derived
  * from this software without specific prior written permission.
  * THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
  * IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
  * WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.
  */

  /*
  * This is derived from the Berkeley source:
  *        @(#)random.c        5.5 (Berkeley) 7/6/88
  * It was reworked for the GNU C Library by Roland McGrath.
  * Rewritten to use reentrant functions by Ulrich Drepper, 1995.
  */

  /*******************************************************************************
  * Modified for McStas from glibc 2.0.7pre1 stdlib/random.c and
  * stdlib/random_r.c.
  *
  * This way random() is more than four times faster compared to calling
  * standard glibc random() on ix86 Linux, probably due to multithread support,
  * ELF shared library overhead, etc. It also makes McStas generated
  * simulations more portable (more likely to behave identically across
  * platforms, important for parrallel computations).
  *******************************************************************************/


#define        TYPE_3                3
#define        BREAK_3                128
#define        DEG_3                31
#define        SEP_3                3

static mc_int32_t randtbl[DEG_3 + 1] =
{
	TYPE_3,

	-1726662223, 379960547, 1735697613, 1040273694, 1313901226,
	1627687941, -179304937, -2073333483, 1780058412, -1989503057,
	-615974602, 344556628, 939512070, -1249116260, 1507946756,
	-812545463, 154635395, 1388815473, -1926676823, 525320961,
	-1009028674, 968117788, -123449607, 1284210865, 435012392,
	-2017506339, -911064859, -370259173, 1132637927, 1398500161,
	-205601318,
};

static mc_int32_t *fptr = &randtbl[SEP_3 + 1];
static mc_int32_t *rptr = &randtbl[1];
static mc_int32_t *state = &randtbl[1];
#define rand_deg DEG_3
#define rand_sep SEP_3
static mc_int32_t *end_ptr = &randtbl[sizeof(randtbl) / sizeof(randtbl[0])];

mc_int32_t
mc_random(void)
{
	mc_int32_t result;

	*fptr += *rptr;
	/* Chucking least random bit.  */
	result = (*fptr >> 1) & 0x7fffffff;
	++fptr;
	if (fptr >= end_ptr)
	{
		fptr = state;
		++rptr;
	}
	else
	{
		++rptr;
		if (rptr >= end_ptr)
			rptr = state;
	}
	return result;
}

void
mc_srandom(unsigned int x)
{
	/* We must make sure the seed is not 0.  Take arbitrarily 1 in this case.  */
	state[0] = x ? x : 1;
	{
		long int i;
		for (i = 1; i < rand_deg; ++i)
		{
			/* This does:
			state[i] = (16807 * state[i - 1]) % 2147483647;
			but avoids overflowing 31 bits.  */
			long int hi = state[i - 1] / 127773;
			long int lo = state[i - 1] % 127773;
			long int test = 16807 * lo - 2836 * hi;
			state[i] = test + (test < 0 ? 2147483647 : 0);
		}
		fptr = &state[rand_sep];
		rptr = &state[0];
		for (i = 0; i < 10 * rand_deg; ++i)
			random();
	}
}

/* "Mersenne Twister", by Makoto Matsumoto and Takuji Nishimura. */
/* See http://www.math.keio.ac.jp/~matumoto/emt.html for original source. */


/*
A C-program for MT19937, with initialization improved 2002/1/26.
Coded by Takuji Nishimura and Makoto Matsumoto.

Before using, initialize the state by using mt_srandom(seed)
or init_by_array(init_key, key_length).

Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. The names of its contributors may not be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Any feedback is very welcome.
http://www.math.keio.ac.jp/matumoto/emt.html
email: matumoto@math.keio.ac.jp
*/

#include <stdio.h>

/* Period parameters */
#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfUL   /* constant vector a */
#define UPPER_MASK 0x80000000UL /* most significant w-r bits */
#define LOWER_MASK 0x7fffffffUL /* least significant r bits */

static unsigned long mt[N]; /* the array for the state vector  */
static int mti = N + 1; /* mti==N+1 means mt[N] is not initialized */

						/* initializes mt[N] with a seed */
void mt_srandom(unsigned long s)
{
	mt[0] = s & 0xffffffffUL;
	for (mti = 1; mti<N; mti++) {
		mt[mti] =
			(1812433253UL * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti);
		/* See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier. */
		/* In the previous versions, MSBs of the seed affect   */
		/* only MSBs of the array mt[].                        */
		/* 2002/01/09 modified by Makoto Matsumoto             */
		mt[mti] &= 0xffffffffUL;
		/* for >32 bit machines */
	}
}

/* initialize by an array with array-length */
/* init_key is the array for initializing keys */
/* key_length is its length */
void init_by_array(unsigned long init_key[], unsigned long key_length)
{
	int i, j, k;
	mt_srandom(19650218UL);
	i = 1; j = 0;
	k = (N>key_length ? N : key_length);
	for (; k; k--) {
		mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525UL))
			+ init_key[j] + j; /* non linear */
		mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
		i++; j++;
		if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
		if (j >= key_length) j = 0;
	}
	for (k = N - 1; k; k--) {
		mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941UL))
			- i; /* non linear */
		mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
		i++;
		if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
	}

	mt[0] = 0x80000000UL; /* MSB is 1; assuring non-zero initial array */
}

/* generates a random number on [0,0xffffffff]-interval */
unsigned long mt_random(void)
{
	unsigned long y;
	static unsigned long mag01[2] = { 0x0UL, MATRIX_A };
	/* mag01[x] = x * MATRIX_A  for x=0,1 */

	if (mti >= N) { /* generate N words at one time */
		int kk;

		if (mti == N + 1)   /* if mt_srandom() has not been called, */
			mt_srandom(5489UL); /* a default initial seed is used */

		for (kk = 0; kk<N - M; kk++) {
			y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
			mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1UL];
		}
		for (; kk<N - 1; kk++) {
			y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
			mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
		}
		y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
		mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

		mti = 0;
	}

	y = mt[mti++];

	/* Tempering */
	y ^= (y >> 11);
	y ^= (y << 7) & 0x9d2c5680UL;
	y ^= (y << 15) & 0xefc60000UL;
	y ^= (y >> 18);

	return y;
}

#undef N
#undef M
#undef MATRIX_A
#undef UPPER_MASK
#undef LOWER_MASK

/* End of "Mersenne Twister". */

/* End of McCode random number routine. */

/* randnorm: generate a random number from normal law */
double
randnorm(void)
{
	static double v1, v2, s;
	static int phase = 0;
	double X, u1, u2;

	if (phase == 0)
	{
		do
		{
			u1 = rand01();
			u2 = rand01();
			v1 = 2 * u1 - 1;
			v2 = 2 * u2 - 1;
			s = v1*v1 + v2*v2;
		} while (s >= 1 || s == 0);

		X = v1*sqrt(-2 * log(s) / s);
	}
	else
	{
		X = v2*sqrt(-2 * log(s) / s);
	}

	phase = 1 - phase;
	return X;
}

/**
* Generate a random number from -1 to 1 with triangle distribution
*/
double randtriangle(void) {
	double randnum = rand01();
	if (randnum>0.5) return(1 - sqrt(2 * (randnum - 0.5)));
	else return(sqrt(2 * randnum) - 1);
}

/**
* Random number between 0.0 and 1.0 (including?)
*/
double rand01() {
	double randnum;
	randnum = (double)random();
	randnum /= (double)MC_RAND_MAX + 1;
	return randnum;
}

/**
* Return a random number between 1 and -1
*/
double randpm1() {
	double randnum;
	randnum = (double)random();
	randnum /= ((double)MC_RAND_MAX + 1) / 2;
	randnum -= 1;
	return randnum;
}

/**
* Return a random number between 0 and max.
*/
double rand0max(double max) {
	double randnum;
	randnum = (double)random();
	randnum /= ((double)MC_RAND_MAX + 1) / max;
	return randnum;
}

/**
* Return a random number between min and max.
*/
double randminmax(double min, double max) {
	return rand0max(max - min) + max;
}

/* SECTION: main and signal handlers ======================================== */

/*******************************************************************************
* mchelp: displays instrument executable help with possible options
*******************************************************************************/
static void
mchelp(char *pgmname)
{
	int i;

	fprintf(stderr, "%s (%s) instrument simulation, generated with " MCCODE_STRING " (" MCCODE_DATE ")\n", mcinstrument_name, mcinstrument_source);
	fprintf(stderr, "Usage: %s [options] [parm=value ...]\n", pgmname);
	fprintf(stderr,
		"Options are:\n"
		"  -s SEED   --seed=SEED      Set random seed (must be != 0)\n"
		"  -n COUNT  --ncount=COUNT   Set number of " MCCODE_PARTICLE "s to simulate.\n"
		"  -d DIR    --dir=DIR        Put all data files in directory DIR.\n"
		"  -t        --trace          Enable trace of " MCCODE_PARTICLE "s through instrument.\n"
		"  -g        --gravitation    Enable gravitation for all trajectories.\n"
		"  --no-output-files          Do not write any data files.\n"
		"  -h        --help           Show this help message.\n"
		"  -i        --info           Detailed instrument information.\n"
		"  --format=FORMAT            Output data files using FORMAT="
		FLAVOR_UPPER
#ifdef USE_NEXUS
		" NEXUS"
#endif
		"\n\n"
	);
#ifdef USE_MPI
	fprintf(stderr,
		"This instrument has been compiled with MPI support.\n  Use 'mpirun %s [options] [parm=value ...]'.\n", pgmname);
#endif
	if (mcnumipar > 0)
	{
		fprintf(stderr, "Instrument parameters are:\n");
		for (i = 0; i < mcnumipar; i++)
			if (mcinputtable[i].val && strlen(mcinputtable[i].val))
				fprintf(stderr, "  %-16s(%s) [default='%s']\n", mcinputtable[i].name,
				(*mcinputtypes[mcinputtable[i].type].parminfo)(mcinputtable[i].name),
					mcinputtable[i].val);
			else
				fprintf(stderr, "  %-16s(%s)\n", mcinputtable[i].name,
				(*mcinputtypes[mcinputtable[i].type].parminfo)(mcinputtable[i].name));
	}

#ifndef NOSIGNALS
	fprintf(stderr, "Known signals are: "
#ifdef SIGUSR1
		"USR1 (status) "
#endif
#ifdef SIGUSR2
		"USR2 (save) "
#endif
#ifdef SIGBREAK
		"BREAK (save) "
#endif
#ifdef SIGTERM
		"TERM (save and exit)"
#endif
		"\n");
#endif /* !NOSIGNALS */
} /* mchelp */


  /* mcshowhelp: show help and exit with 0 */
static void
mcshowhelp(char *pgmname)
{
	mchelp(pgmname);
	exit(0);
}

/* mcusage: display usage when error in input arguments and exit with 1 */
static void
mcusage(char *pgmname)
{
	fprintf(stderr, "Error: incorrect command line arguments\n");
	mchelp(pgmname);
	exit(1);
}

/* mcenabletrace: enable trace/mcdisplay or error if requires recompile */
static void
mcenabletrace(void)
{
	if (mctraceenabled)
		mcdotrace = 1;
	else
	{
		fprintf(stderr,
			"Error: trace not enabled (mcenabletrace)\n"
			"Please re-run the " MCCODE_NAME " compiler "
			"with the --trace option, or rerun the\n"
			"C compiler with the MC_TRACE_ENABLED macro defined.\n");
		exit(1);
	}
}

/*******************************************************************************
* mcreadparams: request parameters from the prompt (or use default)
*******************************************************************************/
void
mcreadparams(void)
{
	int i, j, status;
	static char buf[CHAR_BUF_LENGTH];
	char *p;
	int len;

	MPI_MASTER(printf("Instrument parameters for %s (%s)\n",
		mcinstrument_name, mcinstrument_source));

	for (i = 0; mcinputtable[i].name != 0; i++)
	{
		do
		{
			MPI_MASTER(
				if (mcinputtable[i].val && strlen(mcinputtable[i].val))
					printf("Set value of instrument parameter %s (%s) [default='%s']:\n",
						mcinputtable[i].name,
						(*mcinputtypes[mcinputtable[i].type].parminfo)
						(mcinputtable[i].name), mcinputtable[i].val);
				else
					printf("Set value of instrument parameter %s (%s):\n",
						mcinputtable[i].name,
						(*mcinputtypes[mcinputtable[i].type].parminfo)
						(mcinputtable[i].name));
			fflush(stdout);
			);
#ifdef USE_MPI
			if (mpi_node_rank == mpi_node_root)
			{
				p = fgets(buf, CHAR_BUF_LENGTH, stdin);
				if (p == NULL)
				{
					fprintf(stderr, "Error: empty input for paramater %s (mcreadparams)\n", mcinputtable[i].name);
					exit(1);
				}
			}
			else
				p = buf;
			MPI_Bcast(buf, CHAR_BUF_LENGTH, MPI_CHAR, mpi_node_root, MPI_COMM_WORLD);
#else /* !USE_MPI */
			p = fgets(buf, CHAR_BUF_LENGTH, stdin);
			if (p == NULL)
			{
				fprintf(stderr, "Error: empty input for paramater %s (mcreadparams)\n", mcinputtable[i].name);
				exit(1);
			}
#endif /* USE_MPI */
			len = strlen(buf);
			if (!len || (len == 1 && (buf[0] == '\n' || buf[0] == '\r')))
			{
				if (mcinputtable[i].val && strlen(mcinputtable[i].val)) {
					strncpy(buf, mcinputtable[i].val, CHAR_BUF_LENGTH);  /* use default value */
					len = strlen(buf);
				}
			}
			for (j = 0; j < 2; j++)
			{
				if (len > 0 && (buf[len - 1] == '\n' || buf[len - 1] == '\r'))
				{
					len--;
					buf[len] = '\0';
				}
			}

			status = (*mcinputtypes[mcinputtable[i].type].getparm)
				(buf, mcinputtable[i].par);
			if (!status)
			{
				(*mcinputtypes[mcinputtable[i].type].error)(mcinputtable[i].name, buf);
				if (!mcinputtable[i].val || strlen(mcinputtable[i].val)) {
					fprintf(stderr, "       Change %s default value in instrument definition.\n", mcinputtable[i].name);
					exit(1);
				}
			}
		} while (!status);
	}
} /* mcreadparams */

  /*******************************************************************************
  * mcparseoptions: parse command line arguments (options, parameters)
  *******************************************************************************/
void
mcparseoptions(int argc, char *argv[])
{
	int i, j;
	char *p;
	int paramset = 0, *paramsetarray;
	char *usedir = NULL;

	/* Add one to mcnumipar to avoid allocating zero size memory block. */
	paramsetarray = (int*)malloc((mcnumipar + 1) * sizeof(*paramsetarray));
	if (paramsetarray == NULL)
	{
		fprintf(stderr, "Error: insufficient memory (mcparseoptions)\n");
		exit(1);
	}
	for (j = 0; j < mcnumipar; j++)
	{
		paramsetarray[j] = 0;
		if (mcinputtable[j].val != NULL && strlen(mcinputtable[j].val))
		{
			int  status;
			char buf[CHAR_BUF_LENGTH];
			strncpy(buf, mcinputtable[j].val, CHAR_BUF_LENGTH);
			status = (*mcinputtypes[mcinputtable[j].type].getparm)
				(buf, mcinputtable[j].par);
			if (!status) fprintf(stderr, "Invalid '%s' default value %s in instrument definition (mcparseoptions)\n", mcinputtable[j].name, buf);
			else paramsetarray[j] = 1;
		}
		else {
			(*mcinputtypes[mcinputtable[j].type].getparm)
				(NULL, mcinputtable[j].par);
			paramsetarray[j] = 0;
		}
	}
	for (i = 1; i < argc; i++)
	{
		if (!strcmp("-s", argv[i]) && (i + 1) < argc)
			mcsetseed(argv[++i]);
		else if (!strncmp("-s", argv[i], 2))
			mcsetseed(&argv[i][2]);
		else if (!strcmp("--seed", argv[i]) && (i + 1) < argc)
			mcsetseed(argv[++i]);
		else if (!strncmp("--seed=", argv[i], 7))
			mcsetseed(&argv[i][7]);
		else if (!strcmp("-n", argv[i]) && (i + 1) < argc)
			mcsetn_arg(argv[++i]);
		else if (!strncmp("-n", argv[i], 2))
			mcsetn_arg(&argv[i][2]);
		else if (!strcmp("--ncount", argv[i]) && (i + 1) < argc)
			mcsetn_arg(argv[++i]);
		else if (!strncmp("--ncount=", argv[i], 9))
			mcsetn_arg(&argv[i][9]);
		else if (!strcmp("-d", argv[i]) && (i + 1) < argc)
			usedir = argv[++i];  /* will create directory after parsing all arguments (end of this function) */
		else if (!strncmp("-d", argv[i], 2))
			usedir = &argv[i][2];
		else if (!strcmp("--dir", argv[i]) && (i + 1) < argc)
			usedir = argv[++i];
		else if (!strncmp("--dir=", argv[i], 6))
			usedir = &argv[i][6];
		else if (!strcmp("-h", argv[i]))
			mcshowhelp(argv[0]);
		else if (!strcmp("--help", argv[i]))
			mcshowhelp(argv[0]);
		else if (!strcmp("-i", argv[i])) {
			mcformat = FLAVOR_UPPER;
			mcinfo();
		}
		else if (!strcmp("--info", argv[i]))
			mcinfo();
		else if (!strcmp("-t", argv[i]))
			mcenabletrace();
		else if (!strcmp("--trace", argv[i]))
			mcenabletrace();
		else if (!strcmp("--gravitation", argv[i]))
			mcgravitation = 1;
		else if (!strcmp("-g", argv[i]))
			mcgravitation = 1;
		else if (!strncmp("--format=", argv[i], 9)) {
			mcformat = &argv[i][9];
		}
		else if (!strcmp("--format", argv[i]) && (i + 1) < argc) {
			mcformat = argv[++i];
		}
		else if (!strcmp("--no-output-files", argv[i]))
			mcdisable_output_files = 1;
		else if (argv[i][0] != '-' && (p = strchr(argv[i], '=')) != NULL)
		{
			*p++ = '\0';

			for (j = 0; j < mcnumipar; j++)
				if (!strcmp(mcinputtable[j].name, argv[i]))
				{
					int status;
					status = (*mcinputtypes[mcinputtable[j].type].getparm)(p,
						mcinputtable[j].par);
					if (!status || !strlen(p))
					{
						(*mcinputtypes[mcinputtable[j].type].error)
							(mcinputtable[j].name, p);
						exit(1);
					}
					paramsetarray[j] = 1;
					paramset = 1;
					break;
				}
			if (j == mcnumipar)
			{                                /* Unrecognized parameter name */
				fprintf(stderr, "Error: unrecognized parameter %s (mcparseoptions)\n", argv[i]);
				exit(1);
			}
		}
		else if (argv[i][0] == '-') {
			fprintf(stderr, "Error: unrecognized option argument %s (mcparseoptions). Ignored.\n", argv[i++]);
		}
		else {
			fprintf(stderr, "Error: unrecognized argument %s (mcparseoptions). Aborting.\n", argv[i]);
			mcusage(argv[0]);
		}
	}
	if (!paramset)
		mcreadparams();                /* Prompt for parameters if not specified. */
	else
	{
		for (j = 0; j < mcnumipar; j++)
			if (!paramsetarray[j])
			{
				fprintf(stderr, "Error: Instrument parameter %s left unset (mcparseoptions)\n",
					mcinputtable[j].name);
				exit(1);
			}
	}
	free(paramsetarray);
#ifdef USE_MPI
	if (mcdotrace) mpi_node_count = 1; /* disable threading when in trace mode */
#endif
	if (usedir && strlen(usedir)) mcuse_dir(usedir);
} /* mcparseoptions */

#ifndef NOSIGNALS
mcstatic char  mcsig_message[256];


/*******************************************************************************
* sighandler: signal handler that makes simulation stop, and save results
*******************************************************************************/
void sighandler(int sig)
{
	/* MOD: E. Farhi, Sep 20th 2001: give more info */
	time_t t1, t0;
#define SIG_SAVE 0
#define SIG_TERM 1
#define SIG_STAT 2
#define SIG_ABRT 3

	printf("\n# " MCCODE_STRING ": [pid %i] Signal %i detected", getpid(), sig);
#ifdef USE_MPI
	printf(" [proc %i]", mpi_node_rank);
#endif
#if defined(SIGUSR1) && defined(SIGUSR2) && defined(SIGKILL)
	if (!strcmp(mcsig_message, "sighandler") && (sig != SIGUSR1) && (sig != SIGUSR2))
	{
		printf("\n# Fatal : unrecoverable loop ! Suicide (naughty boy).\n");
		kill(0, SIGKILL); /* kill myself if error occurs within sighandler: loops */
	}
#endif
	switch (sig) {
#ifdef SIGINT
	case SIGINT: printf(" SIGINT (interrupt from terminal, Ctrl-C)"); sig = SIG_TERM; break;
#endif
#ifdef SIGILL
	case SIGILL: printf(" SIGILL (Illegal instruction)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGFPE
	case SIGFPE: printf(" SIGFPE (Math Error)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGSEGV
	case SIGSEGV: printf(" SIGSEGV (Mem Error)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGTERM
	case SIGTERM: printf(" SIGTERM (Termination)"); sig = SIG_TERM; break;
#endif
#ifdef SIGABRT
	case SIGABRT: printf(" SIGABRT (Abort)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGQUIT
	case SIGQUIT: printf(" SIGQUIT (Quit from terminal)"); sig = SIG_TERM; break;
#endif
#ifdef SIGTRAP
	case SIGTRAP: printf(" SIGTRAP (Trace trap)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGPIPE
	case SIGPIPE: printf(" SIGPIPE (Broken pipe)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGUSR1
	case SIGUSR1: printf(" SIGUSR1 (Display info)"); sig = SIG_STAT; break;
#endif
#ifdef SIGUSR2
	case SIGUSR2: printf(" SIGUSR2 (Save simulation)"); sig = SIG_SAVE; break;
#endif
#ifdef SIGHUP
	case SIGHUP: printf(" SIGHUP (Hangup/update)"); sig = SIG_SAVE; break;
#endif
#ifdef SIGBUS
	case SIGBUS: printf(" SIGBUS (Bus error)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGURG
	case SIGURG: printf(" SIGURG (Urgent socket condition)"); sig = SIG_ABRT; break;
#endif
#ifdef SIGBREAK
	case SIGBREAK: printf(" SIGBREAK (Break signal, Ctrl-Break)"); sig = SIG_SAVE; break;
#endif
	default: printf(" (look at signal list for signification)"); sig = SIG_ABRT; break;
	}
	printf("\n");
	printf("# Simulation: %s (%s) \n", mcinstrument_name, mcinstrument_source);
	printf("# Breakpoint: %s ", mcsig_message);
	if (strstr(mcsig_message, "Save") && (sig == SIG_SAVE))
		sig = SIG_STAT;
	SIG_MESSAGE("sighandler");
	if (mcget_ncount() == 0)
		printf("(0 %%)\n");
	else
	{
		printf("%.2f %% (%10.1f/%10.1f)\n", 100.0*mcget_run_num() / mcget_ncount(), 1.0*mcget_run_num(), 1.0*mcget_ncount());
	}
	t0 = (time_t)mcstartdate;
	t1 = time(NULL);
	printf("# Date:      %s", ctime(&t1));
	printf("# Started:   %s", ctime(&t0));

	if (sig == SIG_STAT)
	{
		printf("# " MCCODE_STRING ": Resuming simulation (continue)\n");
		fflush(stdout);
		return;
	}
	else
		if (sig == SIG_SAVE)
		{
			printf("# " MCCODE_STRING ": Saving data and resume simulation (continue)\n");
			mcsave(NULL);
			fflush(stdout);
			return;
		}
		else
			if (sig == SIG_TERM)
			{
				printf("# " MCCODE_STRING ": Finishing simulation (save results and exit)\n");
				mcfinally();
				exit(0);
			}
			else
			{
				fflush(stdout);
				perror("# Last I/O Error");
				printf("# " MCCODE_STRING ": Simulation stop (abort).\n");
				// This portion of the signal handling only works on UNIX
#if defined(__unix__) || defined(__APPLE__)
				signal(sig, SIG_DFL); /* force to use default sighandler now */
				kill(getpid(), sig);  /* and trigger it with the current signal */
#endif
				exit(-1);
			}
#undef SIG_SAVE
#undef SIG_TERM
#undef SIG_STAT
#undef SIG_ABRT

} /* sighandler */
#endif /* !NOSIGNALS */

  /*******************************************************************************
  * mccode_main: McCode main() function.
  *******************************************************************************/
int mccode_main(int argc, char *argv[])
{
	/*  double run_num = 0; */
	time_t  t;
#ifdef USE_MPI
	char mpi_node_name[MPI_MAX_PROCESSOR_NAME];
	int  mpi_node_name_len;
#endif /* USE_MPI */

#ifdef MAC
	argc = ccommand(&argv);
#endif

#ifdef USE_MPI
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &mpi_node_count); /* get number of nodes */
	MPI_Comm_rank(MPI_COMM_WORLD, &mpi_node_rank);
	MPI_Comm_set_name(MPI_COMM_WORLD, mcinstrument_name);
	MPI_Get_processor_name(mpi_node_name, &mpi_node_name_len);
#endif /* USE_MPI */

	t = time(NULL);
	mcseed = (long)t + (long)getpid();

#ifdef USE_MPI
	/* *** print number of nodes *********************************************** */
	if (mpi_node_count > 1) {
		MPI_MASTER(
			printf("Simulation '%s' (%s): running on %i nodes (master is '%s', MPI version %i.%i).\n",
				mcinstrument_name, mcinstrument_source, mpi_node_count, mpi_node_name, MPI_VERSION, MPI_SUBVERSION);
		);
	}
#endif /* USE_MPI */

	mcstartdate = (long)t;  /* set start date before parsing options and creating sim file */

							/* *** parse options ******************************************************* */
	SIG_MESSAGE("main (Start)");
	mcformat = getenv(FLAVOR_UPPER "_FORMAT") ?
		getenv(FLAVOR_UPPER "_FORMAT") : FLAVOR_UPPER;
	mcinstrument_exe = argv[0]; /* store the executable path */
								/* read simulation parameters and options */
	mcparseoptions(argc, argv); /* sets output dir and format */

#ifdef USE_MPI
	if (mpi_node_count > 1) {
		/* share the same seed, then adapt random seed for each node */
		MPI_Bcast(&mcseed, 1, MPI_LONG, 0, MPI_COMM_WORLD); /* root sends its seed to slaves */
		mcseed += mpi_node_rank; /* make sure we use different seeds per node */
	}
#endif
	srandom(mcseed);

	/* *** install sig handler, but only once !! after parameters parsing ******* */
#ifndef NOSIGNALS
#ifdef SIGQUIT
	if (signal(SIGQUIT, sighandler) == SIG_IGN)
		signal(SIGQUIT, SIG_IGN);   /* quit (ASCII FS) */
#endif
#ifdef SIGABRT
	if (signal(SIGABRT, sighandler) == SIG_IGN)
		signal(SIGABRT, SIG_IGN);   /* used by abort, replace SIGIOT in the future */
#endif
#ifdef SIGTERM
	if (signal(SIGTERM, sighandler) == SIG_IGN)
		signal(SIGTERM, SIG_IGN);   /* software termination signal from kill */
#endif
#ifdef SIGUSR1
	if (signal(SIGUSR1, sighandler) == SIG_IGN)
		signal(SIGUSR1, SIG_IGN);   /* display simulation status */
#endif
#ifdef SIGUSR2
	if (signal(SIGUSR2, sighandler) == SIG_IGN)
		signal(SIGUSR2, SIG_IGN);
#endif
#ifdef SIGHUP
	if (signal(SIGHUP, sighandler) == SIG_IGN)
		signal(SIGHUP, SIG_IGN);
#endif
#ifdef SIGILL
	if (signal(SIGILL, sighandler) == SIG_IGN)
		signal(SIGILL, SIG_IGN);    /* illegal instruction (not reset when caught) */
#endif
#ifdef SIGFPE
	if (signal(SIGFPE, sighandler) == SIG_IGN)
		signal(SIGSEGV, SIG_IGN);    /* floating point exception */
#endif
#ifdef SIGBUS
	if (signal(SIGBUS, sighandler) == SIG_IGN)
		signal(SIGSEGV, SIG_IGN);    /* bus error */
#endif
#ifdef SIGSEGV
	if (signal(SIGSEGV, sighandler) == SIG_IGN)
		signal(SIGSEGV, SIG_IGN);   /* segmentation violation */
#endif
#endif /* !NOSIGNALS */
	mcsiminfo_init(NULL); /* open SIM */
	SIG_MESSAGE("main (Init)");
	mcinit();
#ifndef NOSIGNALS
#ifdef SIGINT
	if (signal(SIGINT, sighandler) == SIG_IGN)
		signal(SIGINT, SIG_IGN);    /* interrupt (rubout) only after INIT */
#endif
#endif /* !NOSIGNALS */

									/* ================ main particle generation/propagation loop ================ */
#if defined (USE_MPI)
									/* sliced Ncount on each MPI node */
	mcncount = mpi_node_count > 1 ?
		floor(mcncount / mpi_node_count) :
		mcncount; /* number of rays per node */
#endif

				  /* main particle event loop */
	while (mcrun_num < mcncount || mcrun_num < mcget_ncount())
	{
#ifndef NEUTRONICS
		mcgenstate();
#endif
		/* old init: mcsetstate(0, 0, 0, 0, 0, 1, 0, sx=0, sy=1, sz=0, 1); */
		mcraytrace();
		mcrun_num++;
	}

#ifdef USE_MPI
	/* merge run_num from MPI nodes */
	if (mpi_node_count > 1) {
		double mcrun_num_double = (double)mcrun_num;
		mc_MPI_Sum(&mcrun_num_double, 1);
		mcrun_num = (unsigned long long)mcrun_num_double;
	}
#endif

	/* save/finally executed by master node/thread */
	mcfinally();

#ifdef USE_MPI
	MPI_Finalize();
#endif /* USE_MPI */

	return 0;
} /* mccode_main */

#ifdef NEUTRONICS
  /*Main neutronics function steers the McStas calls, initializes parameters etc */
  /* Only called in case NEUTRONICS = TRUE */
void neutronics_main_(float *inx, float *iny, float *inz, float *invx, float *invy, float *invz, float *intime, float *insx, float *insy, float *insz, float *inw, float *outx, float *outy, float *outz, float *outvx, float *outvy, float *outvz, float *outtime, float *outsx, float *outsy, float *outsz, float *outwgt)
{

	extern double mcnx, mcny, mcnz, mcnvx, mcnvy, mcnvz;
	extern double mcnt, mcnsx, mcnsy, mcnsz, mcnp;

	/* External code governs iteration - McStas is iterated once per call to neutronics_main. I.e. below counter must be initiancated for each call to neutronics_main*/
	mcrun_num = 0;

	time_t t;
	t = (time_t)mcstartdate;
	mcstartdate = t;  /* set start date before parsing options and creating sim file */
	mcinit();

	/* *** parse options *** */
	SIG_MESSAGE("main (Start)");
	mcformat = getenv(FLAVOR_UPPER "_FORMAT") ?
		getenv(FLAVOR_UPPER "_FORMAT") : FLAVOR_UPPER;

	/* Set neutron state based on input from neutronics code */
	mcsetstate(*inx, *iny, *inz, *invx, *invy, *invz, *intime, *insx, *insy, *insz, *inw);

	/* main neutron event loop - runs only one iteration */

	//mcstas_raytrace(&mcncount); /* prior to McStas 1.12 */

	mcallowbackprop = 1; //avoid absorbtion from negative dt
	int argc = 1;
	char *argv[0];
	int dummy = mccode_main(argc, argv);

	*outx = mcnx;
	*outy = mcny;
	*outz = mcnz;
	*outvx = mcnvx;
	*outvy = mcnvy;
	*outvz = mcnvz;
	*outtime = mcnt;
	*outsx = mcnsx;
	*outsy = mcnsy;
	*outsz = mcnsz;
	*outwgt = mcnp;

	return;
} /* neutronics_main */

#endif /*NEUTRONICS*/

#endif /* !MCCODE_H */
  /* End of file "mccode-r.c". */
  /* End of file "mccode-r.c". */

#line 4831 "/home/mcstas/test.c"

#line 1 "mcstas-r.c"
  /*******************************************************************************
  *
  * McStas, neutron ray-tracing package
  *         Copyright (C) 1997-2009, All rights reserved
  *         Risoe National Laboratory, Roskilde, Denmark
  *         Institut Laue Langevin, Grenoble, France
  *
  * Runtime: share/mcstas-r.c
  *
  * %Identification
  * Written by: KN
  * Date:    Aug 29, 1997
  * Release: McStas X.Y
  * Version: $Revision$
  *
  * Runtime system for McStas.
  * Embedded within instrument in runtime mode.
  *
  * Usage: Automatically embbeded in the c code whenever required.
  *
  * $Id$
  *
  *******************************************************************************/

#ifndef MCSTAS_R_H
#include "mcstas-r.h"
#endif
#ifdef DANSE
#include "mcstas-globals.h"
#endif

  /*******************************************************************************
  * The I/O format definitions and functions
  *******************************************************************************/

  /*the magnet stack*/
#ifdef MC_POL_COMPAT
void(*mcMagnetPrecession) (double, double, double, double, double, double,
	double, double*, double*, double*, double, Coords, Rotation) = NULL;
Coords   mcMagnetPos;
Rotation mcMagnetRot;
double*  mcMagnetData = NULL;
/* mcMagneticField(x, y, z, t, Bx, By, Bz) */
int(*mcMagneticField) (double, double, double, double,
	double*, double*, double*, void *) = NULL;
#endif

#ifndef MCSTAS_H

/*******************************************************************************
* mcstore_neutron: stores neutron coodinates into global array (per component)
*******************************************************************************/
void
mcstore_neutron(MCNUM *s, int index, double x, double y, double z,
	double vx, double vy, double vz, double t,
	double sx, double sy, double sz, double p)
{
	double *dptr = &s[11 * index];
	*dptr++ = x;
	*dptr++ = y;
	*dptr++ = z;
	*dptr++ = vx;
	*dptr++ = vy;
	*dptr++ = vz;
	*dptr++ = t;
	*dptr++ = sx;
	*dptr++ = sy;
	*dptr++ = sz;
	*dptr = p;
} /* mcstore_neutron */

  /*******************************************************************************
  * mcrestore_neutron: restores neutron coodinates from global array
  *******************************************************************************/
void
mcrestore_neutron(MCNUM *s, int index, double *x, double *y, double *z,
	double *vx, double *vy, double *vz, double *t,
	double *sx, double *sy, double *sz, double *p)
{
	double *dptr = &s[11 * index];
	*x = *dptr++;
	*y = *dptr++;
	*z = *dptr++;
	*vx = *dptr++;
	*vy = *dptr++;
	*vz = *dptr++;
	*t = *dptr++;
	*sx = *dptr++;
	*sy = *dptr++;
	*sz = *dptr++;
	*p = *dptr;
} /* mcrestore_neutron */

  /*******************************************************************************
  * mcsetstate: transfer parameters into global McStas variables
  *******************************************************************************/
void
mcsetstate(double x, double y, double z, double vx, double vy, double vz,
	double t, double sx, double sy, double sz, double p)
{
	extern double mcnx, mcny, mcnz, mcnvx, mcnvy, mcnvz;
	extern double mcnt, mcnsx, mcnsy, mcnsz, mcnp;

	mcnx = x;
	mcny = y;
	mcnz = z;
	mcnvx = vx;
	mcnvy = vy;
	mcnvz = vz;
	mcnt = t;
	mcnsx = sx;
	mcnsy = sy;
	mcnsz = sz;
	mcnp = p;
} /* mcsetstate */

  /*******************************************************************************
  * mcgenstate: set default neutron parameters
  *******************************************************************************/
void
mcgenstate(void)
{
	mcsetstate(0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1);
	/* old initialisation: mcsetstate(0, 0, 0, 0, 0, 1, 0, sx=0, sy=1, sz=0, 1); */
}

/* intersection routines ==================================================== */

/*******************************************************************************
* inside_rectangle: Check if (x,y) is inside rectangle (xwidth, yheight)
* return 0 if outside and 1 if inside
*******************************************************************************/
int inside_rectangle(double x, double y, double xwidth, double yheight)
{
	if (x>-xwidth / 2 && x<xwidth / 2 && y>-yheight / 2 && y<yheight / 2)
		return 1;
	else
		return 0;
}

/*******************************************************************************
* box_intersect: compute time intersection with a box
* returns 0 when no intersection is found
*      or 1 in case of intersection with resulting times dt_in and dt_out
* This function written by Stine Nyborg, 1999.
*******************************************************************************/
int box_intersect(double *dt_in, double *dt_out,
	double x, double y, double z,
	double vx, double vy, double vz,
	double dx, double dy, double dz)
{
	double x_in, y_in, z_in, tt, t[6], a, b;
	int i, count, s;

	/* Calculate intersection time for each of the six box surface planes
	*  If the box surface plane is not hit, the result is zero.*/

	if (vx != 0)
	{
		tt = -(dx / 2 + x) / vx;
		y_in = y + tt*vy;
		z_in = z + tt*vz;
		if (y_in > -dy / 2 && y_in < dy / 2 && z_in > -dz / 2 && z_in < dz / 2)
			t[0] = tt;
		else
			t[0] = 0;

		tt = (dx / 2 - x) / vx;
		y_in = y + tt*vy;
		z_in = z + tt*vz;
		if (y_in > -dy / 2 && y_in < dy / 2 && z_in > -dz / 2 && z_in < dz / 2)
			t[1] = tt;
		else
			t[1] = 0;
	}
	else
		t[0] = t[1] = 0;

	if (vy != 0)
	{
		tt = -(dy / 2 + y) / vy;
		x_in = x + tt*vx;
		z_in = z + tt*vz;
		if (x_in > -dx / 2 && x_in < dx / 2 && z_in > -dz / 2 && z_in < dz / 2)
			t[2] = tt;
		else
			t[2] = 0;

		tt = (dy / 2 - y) / vy;
		x_in = x + tt*vx;
		z_in = z + tt*vz;
		if (x_in > -dx / 2 && x_in < dx / 2 && z_in > -dz / 2 && z_in < dz / 2)
			t[3] = tt;
		else
			t[3] = 0;
	}
	else
		t[2] = t[3] = 0;

	if (vz != 0)
	{
		tt = -(dz / 2 + z) / vz;
		x_in = x + tt*vx;
		y_in = y + tt*vy;
		if (x_in > -dx / 2 && x_in < dx / 2 && y_in > -dy / 2 && y_in < dy / 2)
			t[4] = tt;
		else
			t[4] = 0;

		tt = (dz / 2 - z) / vz;
		x_in = x + tt*vx;
		y_in = y + tt*vy;
		if (x_in > -dx / 2 && x_in < dx / 2 && y_in > -dy / 2 && y_in < dy / 2)
			t[5] = tt;
		else
			t[5] = 0;
	}
	else
		t[4] = t[5] = 0;

	/* The intersection is evaluated and *dt_in and *dt_out are assigned */

	a = b = s = 0;
	count = 0;

	for (i = 0; i < 6; i = i + 1)
		if (t[i] == 0)
			s = s + 1;
		else if (count == 0)
		{
			a = t[i];
			count = 1;
		}
		else
		{
			b = t[i];
			count = 2;
		}

	if (a == 0 && b == 0)
		return 0;
	else if (a < b)
	{
		*dt_in = a;
		*dt_out = b;
		return 1;
	}
	else
	{
		*dt_in = b;
		*dt_out = a;
		return 1;
	}

} /* box_intersect */

  /*******************************************************************************
  * cylinder_intersect: compute intersection with a cylinder
  * returns 0 when no intersection is found
  *      or 2/4/8/16 bits depending on intersection,
  *     and resulting times t0 and t1
  * Written by: EM,NB,ABA 4.2.98
  *******************************************************************************/
int
cylinder_intersect(double *t0, double *t1, double x, double y, double z,
	double vx, double vy, double vz, double r, double h)
{
	double D, t_in, t_out, y_in, y_out;
	int ret = 1;

	D = (2 * vx*x + 2 * vz*z)*(2 * vx*x + 2 * vz*z)
		- 4 * (vx*vx + vz*vz)*(x*x + z*z - r*r);

	if (D >= 0)
	{
		if (vz*vz + vx*vx) {
			t_in = (-(2 * vz*z + 2 * vx*x) - sqrt(D)) / (2 * (vz*vz + vx*vx));
			t_out = (-(2 * vz*z + 2 * vx*x) + sqrt(D)) / (2 * (vz*vz + vx*vx));
		}
		else if (vy) { /* trajectory parallel to cylinder axis */
			t_in = (-h / 2 - y) / vy;
			t_out = (h / 2 - y) / vy;
			if (t_in>t_out) {
				double tmp = t_in;
				t_in = t_out; t_out = tmp;
			}
		}
		else return 0;
		y_in = vy*t_in + y;
		y_out = vy*t_out + y;

		if ((y_in > h / 2 && y_out > h / 2) || (y_in < -h / 2 && y_out < -h / 2))
			return 0;
		else
		{
			if (y_in > h / 2)
			{
				t_in = ((h / 2) - y) / vy; ret += 2;
			}
			else if (y_in < -h / 2)
			{
				t_in = ((-h / 2) - y) / vy; ret += 4;
			}
			if (y_out > h / 2)
			{
				t_out = ((h / 2) - y) / vy; ret += 8;
			}
			else if (y_out < -h / 2)
			{
				t_out = ((-h / 2) - y) / vy; ret += 16;
			}
		}
		*t0 = t_in;
		*t1 = t_out;
		return ret;
	}
	else
	{
		*t0 = *t1 = 0;
		return 0;
	}
} /* cylinder_intersect */


  /*******************************************************************************
  * sphere_intersect: Calculate intersection between a line and a sphere.
  * returns 0 when no intersection is found
  *      or 1 in case of intersection with resulting times t0 and t1
  *******************************************************************************/
int
sphere_intersect(double *t0, double *t1, double x, double y, double z,
	double vx, double vy, double vz, double r)
{
	double A, B, C, D, v;

	v = sqrt(vx*vx + vy*vy + vz*vz);
	A = v*v;
	B = 2 * (x*vx + y*vy + z*vz);
	C = x*x + y*y + z*z - r*r;
	D = B*B - 4 * A*C;
	if (D < 0)
		return 0;
	D = sqrt(D);
	*t0 = (-B - D) / (2 * A);
	*t1 = (-B + D) / (2 * A);
	return 1;
} /* sphere_intersect */

  /*******************************************************************************
  * plane_intersect: Calculate intersection between a plane and a line.
  * returns 0 when no intersection is found (i.e. line is parallel to the plane)
  * returns 1 or -1 when intersection time is positive and negative respectively
  *******************************************************************************/
int
plane_intersect(double *t, double x, double y, double z,
	double vx, double vy, double vz, double nx, double ny, double nz, double wx, double wy, double wz)
{
	double s;
	if (fabs(s = scalar_prod(nx, ny, nz, vx, vy, vz))<FLT_EPSILON) return 0;
	*t = -scalar_prod(nx, ny, nz, x - wx, y - wy, z - wz) / s;
	if (*t<0) return -1;
	else return 1;
} /* plane_intersect */

#endif /* !MCSTAS_H */
  /* End of file "mcstas-r.c". */

#line 5191 "/home/mcstas/test.c"
#ifdef MC_TRACE_ENABLED
int mctraceenabled = 1;
#else
int mctraceenabled = 0;
#endif
#define MCSTAS "/usr/share/mcstas/2.3/"
int mcdefaultmain = 1;
char mcinstrument_name[] = "My_Instrument";
char mcinstrument_source[] = "/home/mcstas/test.instr";
char *mcinstrument_exe = NULL; /* will be set to argv[0] in main */
int main(int argc, char *argv[]) { return mccode_main(argc, argv); }
void mcinit(void);
void mcraytrace(void);
void mcsave(FILE *);
void mcfinally(void);
void mcdisplay(void);

/* Instrument parameters. */
MCNUM mcipDIST;

#define mcNUMIPAR 1
int mcnumipar = 1;
struct mcinputtable_struct mcinputtable[mcNUMIPAR + 1] = {
	"DIST", &mcipDIST, instr_type_double, "10",
	NULL, NULL, instr_type_double, ""
};

/* User declarations from instrument definition. */
#define mccompcurname  My_Instrument
#define mccompcurtype  INSTRUMENT
#define mccompcurindex 0
#define mcposaMy_Instrument coords_set(0,0,0)
#define DIST mcipDIST
#undef DIST
#undef mcposaMy_Instrument
#undef mccompcurindex
#undef mccompcurtype
#undef mccompcurname

/* neutron state table at each component input (local coords) */
/* [x, y, z, vx, vy, vz, t, sx, sy, sz, p] */
MCNUM mccomp_storein[11 * 6];
/* Components position table (absolute and relative coords) */
Coords mccomp_posa[6];
Coords mccomp_posr[6];
/* Counter for each comp to check for inactive ones */
MCNUM  mcNCounter[6];
MCNUM  mcPCounter[6];
MCNUM  mcP2Counter[6];
#define mcNUMCOMP 5 /* number of components */
/* Counter for PROP ABSORB */
MCNUM  mcAbsorbProp[6];
/* Flag true when previous component acted on the neutron (SCATTER) */
MCNUM mcScattered = 0;
/* Flag true when neutron should be restored (RESTORE) */
MCNUM mcRestore = 0;
/* Declarations of component definition and setting parameters. */

/* Setting parameters for component 'Source' [2]. */
MCNUM mccSource_radius;
MCNUM mccSource_yheight;
MCNUM mccSource_xwidth;
MCNUM mccSource_dist;
MCNUM mccSource_focus_xw;
MCNUM mccSource_focus_yh;
MCNUM mccSource_E0;
MCNUM mccSource_dE;
MCNUM mccSource_lambda0;
MCNUM mccSource_dlambda;
MCNUM mccSource_flux;
MCNUM mccSource_gauss;
int mccSource_target_index;

/* Definition parameters for component 'Emon' [3]. */
#define mccEmon_nE 20
/* Setting parameters for component 'Emon' [3]. */
char mccEmon_filename[16384];
MCNUM mccEmon_xmin;
MCNUM mccEmon_xmax;
MCNUM mccEmon_ymin;
MCNUM mccEmon_ymax;
MCNUM mccEmon_xwidth;
MCNUM mccEmon_yheight;
MCNUM mccEmon_Emin;
MCNUM mccEmon_Emax;
MCNUM mccEmon_restore_neutron;

/* Definition parameters for component 'PSD' [4]. */
#define mccPSD_nx 128
#define mccPSD_ny 128
/* Setting parameters for component 'PSD' [4]. */
char mccPSD_filename[16384];
MCNUM mccPSD_xmin;
MCNUM mccPSD_xmax;
MCNUM mccPSD_ymin;
MCNUM mccPSD_ymax;
MCNUM mccPSD_xwidth;
MCNUM mccPSD_yheight;
MCNUM mccPSD_restore_neutron;

/* User component declarations. */

/* User declarations for component 'Origin' [1]. */
#define mccompcurname  Origin
#define mccompcurtype  Arm
#define mccompcurindex 1
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

/* User declarations for component 'Source' [2]. */
#define mccompcurname  Source
#define mccompcurtype  Source_simple
#define mccompcurindex 2
#define pmul mccSource_pmul
#define square mccSource_square
#define srcArea mccSource_srcArea
#define radius mccSource_radius
#define yheight mccSource_yheight
#define xwidth mccSource_xwidth
#define dist mccSource_dist
#define focus_xw mccSource_focus_xw
#define focus_yh mccSource_focus_yh
#define E0 mccSource_E0
#define dE mccSource_dE
#define lambda0 mccSource_lambda0
#define dlambda mccSource_dlambda
#define flux mccSource_flux
#define gauss mccSource_gauss
#define target_index mccSource_target_index
#line 67 "/usr/share/mcstas/2.3/sources/Source_simple.comp"
double pmul, srcArea;
int square;
#line 5325 "/home/mcstas/test.c"
#undef target_index
#undef gauss
#undef flux
#undef dlambda
#undef lambda0
#undef dE
#undef E0
#undef focus_yh
#undef focus_xw
#undef dist
#undef xwidth
#undef yheight
#undef radius
#undef srcArea
#undef square
#undef pmul
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

/* User declarations for component 'Emon' [3]. */
#define mccompcurname  Emon
#define mccompcurtype  E_monitor
#define mccompcurindex 3
#define nE mccEmon_nE
#define E_N mccEmon_E_N
#define E_p mccEmon_E_p
#define E_p2 mccEmon_E_p2
#define S_p mccEmon_S_p
#define S_pE mccEmon_S_pE
#define S_pE2 mccEmon_S_pE2
#define filename mccEmon_filename
#define xmin mccEmon_xmin
#define xmax mccEmon_xmax
#define ymin mccEmon_ymin
#define ymax mccEmon_ymax
#define xwidth mccEmon_xwidth
#define yheight mccEmon_yheight
#define Emin mccEmon_Emin
#define Emax mccEmon_Emax
#define restore_neutron mccEmon_restore_neutron
#line 61 "/usr/share/mcstas/2.3/monitors/E_monitor.comp"
double E_N[nE];
double E_p[nE], E_p2[nE];
double S_p, S_pE, S_pE2;
#line 5371 "/home/mcstas/test.c"
#undef restore_neutron
#undef Emax
#undef Emin
#undef yheight
#undef xwidth
#undef ymax
#undef ymin
#undef xmax
#undef xmin
#undef filename
#undef S_pE2
#undef S_pE
#undef S_p
#undef E_p2
#undef E_p
#undef E_N
#undef nE
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

/* User declarations for component 'PSD' [4]. */
#define mccompcurname  PSD
#define mccompcurtype  PSD_monitor
#define mccompcurindex 4
#define nx mccPSD_nx
#define ny mccPSD_ny
#define PSD_N mccPSD_PSD_N
#define PSD_p mccPSD_PSD_p
#define PSD_p2 mccPSD_PSD_p2
#define filename mccPSD_filename
#define xmin mccPSD_xmin
#define xmax mccPSD_xmax
#define ymin mccPSD_ymin
#define ymax mccPSD_ymax
#define xwidth mccPSD_xwidth
#define yheight mccPSD_yheight
#define restore_neutron mccPSD_restore_neutron
#line 58 "/usr/share/mcstas/2.3/monitors/PSD_monitor.comp"
double PSD_N[nx][ny];
double PSD_p[nx][ny];
double PSD_p2[nx][ny];
#line 5414 "/home/mcstas/test.c"
#undef restore_neutron
#undef yheight
#undef xwidth
#undef ymax
#undef ymin
#undef xmax
#undef xmin
#undef filename
#undef PSD_p2
#undef PSD_p
#undef PSD_N
#undef ny
#undef nx
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

Coords mcposaOrigin, mcposrOrigin;
Rotation mcrotaOrigin, mcrotrOrigin;
Coords mcposaSource, mcposrSource;
Rotation mcrotaSource, mcrotrSource;
Coords mcposaEmon, mcposrEmon;
Rotation mcrotaEmon, mcrotrEmon;
Coords mcposaPSD, mcposrPSD;
Rotation mcrotaPSD, mcrotrPSD;

MCNUM mcnx, mcny, mcnz, mcnvx, mcnvy, mcnvz, mcnt, mcnsx, mcnsy, mcnsz, mcnp;

/* end declare */

void mcinit(void) {
#define mccompcurname  My_Instrument
#define mccompcurtype  INSTRUMENT
#define mccompcurindex 0
#define mcposaMy_Instrument coords_set(0,0,0)
#define DIST mcipDIST
#undef DIST
#undef mcposaMy_Instrument
#undef mccompcurindex
#undef mccompcurtype
#undef mccompcurname
	/* Computation of coordinate transformations. */
	{
		Coords mctc1, mctc2;
		Rotation mctr1;

		mcDEBUG_INSTR()
			/* Component initializations. */
			/* Component Origin. */
			/* Setting parameters for component Origin. */
			SIG_MESSAGE("Origin (Init:SetPar)");

		SIG_MESSAGE("Origin (Init:Place/Rotate)");
		rot_set_rotation(mcrotaOrigin,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD);
#line 5472 "/home/mcstas/test.c"
		rot_copy(mcrotrOrigin, mcrotaOrigin);
		mcposaOrigin = coords_set(
#line 8 "/home/mcstas/test.instr"
			0,
#line 8 "/home/mcstas/test.instr"
			0,
#line 8 "/home/mcstas/test.instr"
			0);
#line 5481 "/home/mcstas/test.c"
		mctc1 = coords_neg(mcposaOrigin);
		mcposrOrigin = rot_apply(mcrotaOrigin, mctc1);
		mcDEBUG_COMPONENT("Origin", mcposaOrigin, mcrotaOrigin)
			mccomp_posa[1] = mcposaOrigin;
		mccomp_posr[1] = mcposrOrigin;
		mcNCounter[1] = mcPCounter[1] = mcP2Counter[1] = 0;
		mcAbsorbProp[1] = 0;
		/* Component Source. */
		/* Setting parameters for component Source. */
		SIG_MESSAGE("Source (Init:SetPar)");
#line 12 "/home/mcstas/test.instr"
		mccSource_radius = 0.1;
#line 12 "/home/mcstas/test.instr"
		mccSource_yheight = 0.1;
#line 12 "/home/mcstas/test.instr"
		mccSource_xwidth = 0.1;
#line 12 "/home/mcstas/test.instr"
		mccSource_dist = mcipDIST;
#line 60 "/home/mcstas/test.instr"
		mccSource_focus_xw = .045;
#line 60 "/home/mcstas/test.instr"
		mccSource_focus_yh = .12;
#line 13 "/home/mcstas/test.instr"
		mccSource_E0 = 5;
#line 13 "/home/mcstas/test.instr"
		mccSource_dE = 1;
#line 61 "/home/mcstas/test.instr"
		mccSource_lambda0 = 0;
#line 61 "/home/mcstas/test.instr"
		mccSource_dlambda = 0;
#line 62 "/home/mcstas/test.instr"
		mccSource_flux = 1;
#line 62 "/home/mcstas/test.instr"
		mccSource_gauss = 0;
#line 62 "/home/mcstas/test.instr"
		mccSource_target_index = +1;
#line 5518 "/home/mcstas/test.c"

		SIG_MESSAGE("Source (Init:Place/Rotate)");
		rot_set_rotation(mctr1,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD);
#line 5525 "/home/mcstas/test.c"
		rot_mul(mctr1, mcrotaOrigin, mcrotaSource);
		rot_transpose(mcrotaOrigin, mctr1);
		rot_mul(mcrotaSource, mctr1, mcrotrSource);
		mctc1 = coords_set(
#line 14 "/home/mcstas/test.instr"
			0,
#line 14 "/home/mcstas/test.instr"
			0,
#line 14 "/home/mcstas/test.instr"
			0);
#line 5536 "/home/mcstas/test.c"
		rot_transpose(mcrotaOrigin, mctr1);
		mctc2 = rot_apply(mctr1, mctc1);
		mcposaSource = coords_add(mcposaOrigin, mctc2);
		mctc1 = coords_sub(mcposaOrigin, mcposaSource);
		mcposrSource = rot_apply(mcrotaSource, mctc1);
		mcDEBUG_COMPONENT("Source", mcposaSource, mcrotaSource)
			mccomp_posa[2] = mcposaSource;
		mccomp_posr[2] = mcposrSource;
		mcNCounter[2] = mcPCounter[2] = mcP2Counter[2] = 0;
		mcAbsorbProp[2] = 0;
		/* Component Emon. */
		/* Setting parameters for component Emon. */
		SIG_MESSAGE("Emon (Init:SetPar)");
#line 18 "/home/mcstas/test.instr"
		if ("Emon.dat") strncpy(mccEmon_filename, "Emon.dat" ? "Emon.dat" : "", 16384); else mccEmon_filename[0] = '\0';
#line 18 "/home/mcstas/test.instr"
		mccEmon_xmin = -0.1;
#line 18 "/home/mcstas/test.instr"
		mccEmon_xmax = 0.1;
#line 18 "/home/mcstas/test.instr"
		mccEmon_ymin = -0.1;
#line 19 "/home/mcstas/test.instr"
		mccEmon_ymax = 0.1;
#line 55 "/home/mcstas/test.instr"
		mccEmon_xwidth = 0;
#line 55 "/home/mcstas/test.instr"
		mccEmon_yheight = 0;
#line 19 "/home/mcstas/test.instr"
		mccEmon_Emin = 0;
#line 19 "/home/mcstas/test.instr"
		mccEmon_Emax = 10;
#line 55 "/home/mcstas/test.instr"
		mccEmon_restore_neutron = 0;
#line 5570 "/home/mcstas/test.c"

		SIG_MESSAGE("Emon (Init:Place/Rotate)");
		rot_set_rotation(mctr1,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD);
#line 5577 "/home/mcstas/test.c"
		rot_mul(mctr1, mcrotaOrigin, mcrotaEmon);
		rot_transpose(mcrotaSource, mctr1);
		rot_mul(mcrotaEmon, mctr1, mcrotrEmon);
		mctc1 = coords_set(
#line 20 "/home/mcstas/test.instr"
			0,
#line 20 "/home/mcstas/test.instr"
			0,
#line 20 "/home/mcstas/test.instr"
			mcipDIST);
#line 5588 "/home/mcstas/test.c"
		rot_transpose(mcrotaOrigin, mctr1);
		mctc2 = rot_apply(mctr1, mctc1);
		mcposaEmon = coords_add(mcposaOrigin, mctc2);
		mctc1 = coords_sub(mcposaSource, mcposaEmon);
		mcposrEmon = rot_apply(mcrotaEmon, mctc1);
		mcDEBUG_COMPONENT("Emon", mcposaEmon, mcrotaEmon)
			mccomp_posa[3] = mcposaEmon;
		mccomp_posr[3] = mcposrEmon;
		mcNCounter[3] = mcPCounter[3] = mcP2Counter[3] = 0;
		mcAbsorbProp[3] = 0;
		/* Component PSD. */
		/* Setting parameters for component PSD. */
		SIG_MESSAGE("PSD (Init:SetPar)");
#line 24 "/home/mcstas/test.instr"
		if ("PSD.dat") strncpy(mccPSD_filename, "PSD.dat" ? "PSD.dat" : "", 16384); else mccPSD_filename[0] = '\0';
#line 24 "/home/mcstas/test.instr"
		mccPSD_xmin = -0.1;
#line 25 "/home/mcstas/test.instr"
		mccPSD_xmax = 0.1;
#line 25 "/home/mcstas/test.instr"
		mccPSD_ymin = -0.1;
#line 25 "/home/mcstas/test.instr"
		mccPSD_ymax = 0.1;
#line 52 "/home/mcstas/test.instr"
		mccPSD_xwidth = 0;
#line 52 "/home/mcstas/test.instr"
		mccPSD_yheight = 0;
#line 52 "/home/mcstas/test.instr"
		mccPSD_restore_neutron = 0;
#line 5618 "/home/mcstas/test.c"

		SIG_MESSAGE("PSD (Init:Place/Rotate)");
		rot_set_rotation(mctr1,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD,
			(0.0)*DEG2RAD);
#line 5625 "/home/mcstas/test.c"
		rot_mul(mctr1, mcrotaEmon, mcrotaPSD);
		rot_transpose(mcrotaEmon, mctr1);
		rot_mul(mcrotaPSD, mctr1, mcrotrPSD);
		mctc1 = coords_set(
#line 26 "/home/mcstas/test.instr"
			0,
#line 26 "/home/mcstas/test.instr"
			0,
#line 26 "/home/mcstas/test.instr"
			1e-10);
#line 5636 "/home/mcstas/test.c"
		rot_transpose(mcrotaEmon, mctr1);
		mctc2 = rot_apply(mctr1, mctc1);
		mcposaPSD = coords_add(mcposaEmon, mctc2);
		mctc1 = coords_sub(mcposaEmon, mcposaPSD);
		mcposrPSD = rot_apply(mcrotaPSD, mctc1);
		mcDEBUG_COMPONENT("PSD", mcposaPSD, mcrotaPSD)
			mccomp_posa[4] = mcposaPSD;
		mccomp_posr[4] = mcposrPSD;
		mcNCounter[4] = mcPCounter[4] = mcP2Counter[4] = 0;
		mcAbsorbProp[4] = 0;
		/* Component initializations. */
		/* Initializations for component Origin. */
		SIG_MESSAGE("Origin (Init)");

		/* Initializations for component Source. */
		SIG_MESSAGE("Source (Init)");
#define mccompcurname  Source
#define mccompcurtype  Source_simple
#define mccompcurindex 2
#define pmul mccSource_pmul
#define square mccSource_square
#define srcArea mccSource_srcArea
#define radius mccSource_radius
#define yheight mccSource_yheight
#define xwidth mccSource_xwidth
#define dist mccSource_dist
#define focus_xw mccSource_focus_xw
#define focus_yh mccSource_focus_yh
#define E0 mccSource_E0
#define dE mccSource_dE
#define lambda0 mccSource_lambda0
#define dlambda mccSource_dlambda
#define flux mccSource_flux
#define gauss mccSource_gauss
#define target_index mccSource_target_index
#line 71 "/usr/share/mcstas/2.3/sources/Source_simple.comp"
		{
			square = 0;
			/* Determine source area */
			if (radius && !yheight && !xwidth) {
				square = 0;
				srcArea = PI*radius*radius;
			}
			else if (yheight && xwidth) {
				square = 1;
				srcArea = xwidth * yheight;
			}

			if (flux) {
				pmul = flux*1e4*srcArea / mcget_ncount();
				if (dlambda)
					pmul *= 2 * dlambda;
				else if (dE)
					pmul *= 2 * dE;
			}
			else {
				gauss = 0;
				pmul = 1.0 / (mcget_ncount() * 4 * PI);
			}

			if (target_index && !dist)
			{
				Coords ToTarget;
				double tx, ty, tz;
				ToTarget = coords_sub(POS_A_COMP_INDEX(INDEX_CURRENT_COMP + target_index), POS_A_CURRENT_COMP);
				ToTarget = rot_apply(ROT_A_CURRENT_COMP, ToTarget);
				coords_get(ToTarget, &tx, &ty, &tz);
				dist = sqrt(tx*tx + ty*ty + tz*tz);
			}

			if (srcArea <= 0) {
				printf("Source_simple: %s: Source area is <= 0 !\n ERROR - Exiting\n",
					NAME_CURRENT_COMP);
				exit(0);
			}
			if (dist <= 0 || focus_xw <= 0 || focus_yh <= 0) {
				printf("Source_simple: %s: Target area unmeaningful! (negative dist / focus_xw / focus_yh)\n ERROR - Exiting\n",
					NAME_CURRENT_COMP);
				exit(0);
			}

			if ((!lambda0 && !E0 && !dE && !dlambda)) {
				printf("Source_simple: %s: You must specify either a wavelength or energy range!\n ERROR - Exiting\n",
					NAME_CURRENT_COMP);
				exit(0);
			}
			if ((!lambda0 && !dlambda && (E0 <= 0 || dE < 0 || E0 - dE <= 0))
				|| (!E0 && !dE && (lambda0 <= 0 || dlambda < 0 || lambda0 - dlambda <= 0))) {
				printf("Source_simple: %s: Unmeaningful definition of wavelength or energy range!\n ERROR - Exiting\n",
					NAME_CURRENT_COMP);
				exit(0);
			}
		}
#line 5728 "/home/mcstas/test.c"
#undef target_index
#undef gauss
#undef flux
#undef dlambda
#undef lambda0
#undef dE
#undef E0
#undef focus_yh
#undef focus_xw
#undef dist
#undef xwidth
#undef yheight
#undef radius
#undef srcArea
#undef square
#undef pmul
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		/* Initializations for component Emon. */
		SIG_MESSAGE("Emon (Init)");
#define mccompcurname  Emon
#define mccompcurtype  E_monitor
#define mccompcurindex 3
#define nE mccEmon_nE
#define E_N mccEmon_E_N
#define E_p mccEmon_E_p
#define E_p2 mccEmon_E_p2
#define S_p mccEmon_S_p
#define S_pE mccEmon_S_pE
#define S_pE2 mccEmon_S_pE2
#define filename mccEmon_filename
#define xmin mccEmon_xmin
#define xmax mccEmon_xmax
#define ymin mccEmon_ymin
#define ymax mccEmon_ymax
#define xwidth mccEmon_xwidth
#define yheight mccEmon_yheight
#define Emin mccEmon_Emin
#define Emax mccEmon_Emax
#define restore_neutron mccEmon_restore_neutron
#line 67 "/usr/share/mcstas/2.3/monitors/E_monitor.comp"
		{
			int i;

			if (xwidth  > 0) { xmax = xwidth / 2;  xmin = -xmax; }
			if (yheight > 0) { ymax = yheight / 2; ymin = -ymax; }

			if ((xmin >= xmax) || (ymin >= ymax)) {
				printf("E_monitor: %s: Null detection area !\n"
					"ERROR      (xwidth,yheight,xmin,xmax,ymin,ymax). Exiting",
					NAME_CURRENT_COMP);
				exit(0);
			}

			for (i = 0; i<nE; i++)
			{
				E_N[i] = 0;
				E_p[i] = 0;
				E_p2[i] = 0;
			}
			S_p = S_pE = S_pE2 = 0;
		}
#line 5793 "/home/mcstas/test.c"
#undef restore_neutron
#undef Emax
#undef Emin
#undef yheight
#undef xwidth
#undef ymax
#undef ymin
#undef xmax
#undef xmin
#undef filename
#undef S_pE2
#undef S_pE
#undef S_p
#undef E_p2
#undef E_p
#undef E_N
#undef nE
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		/* Initializations for component PSD. */
		SIG_MESSAGE("PSD (Init)");
#define mccompcurname  PSD
#define mccompcurtype  PSD_monitor
#define mccompcurindex 4
#define nx mccPSD_nx
#define ny mccPSD_ny
#define PSD_N mccPSD_PSD_N
#define PSD_p mccPSD_PSD_p
#define PSD_p2 mccPSD_PSD_p2
#define filename mccPSD_filename
#define xmin mccPSD_xmin
#define xmax mccPSD_xmax
#define ymin mccPSD_ymin
#define ymax mccPSD_ymax
#define xwidth mccPSD_xwidth
#define yheight mccPSD_yheight
#define restore_neutron mccPSD_restore_neutron
#line 63 "/usr/share/mcstas/2.3/monitors/PSD_monitor.comp"
		{
			int i, j;

			if (xwidth  > 0) { xmax = xwidth / 2;  xmin = -xmax; }
			if (yheight > 0) { ymax = yheight / 2; ymin = -ymax; }

			if ((xmin >= xmax) || (ymin >= ymax)) {
				printf("PSD_monitor: %s: Null detection area !\n"
					"ERROR        (xwidth,yheight,xmin,xmax,ymin,ymax). Exiting",
					NAME_CURRENT_COMP);
				exit(0);
			}

			for (i = 0; i<nx; i++)
				for (j = 0; j<ny; j++)
				{
					PSD_N[i][j] = 0;
					PSD_p[i][j] = 0;
					PSD_p2[i][j] = 0;
				}
		}
#line 5855 "/home/mcstas/test.c"
#undef restore_neutron
#undef yheight
#undef xwidth
#undef ymax
#undef ymin
#undef xmax
#undef xmin
#undef filename
#undef PSD_p2
#undef PSD_p
#undef PSD_N
#undef ny
#undef nx
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		if (mcdotrace) mcdisplay();
		mcDEBUG_INSTR_END()
	}

} /* end init */

void mcraytrace(void) {
	/* Neutronics-specific defines */
#ifdef NEUTRONICS
	extern double mcnx, mcny, mcnz, mcnvx, mcnvy, mcnvz;
	extern double mcnt, mcnsx, mcnsy, mcnsz, mcnp;
#endif
	/* End of Neutronics-specific defines */
	/* Copy neutron state to local variables. */
	MCNUM mcnlx = mcnx;
	MCNUM mcnly = mcny;
	MCNUM mcnlz = mcnz;
	MCNUM mcnlvx = mcnvx;
	MCNUM mcnlvy = mcnvy;
	MCNUM mcnlvz = mcnvz;
	MCNUM mcnlt = mcnt;
	MCNUM mcnlsx = mcnsx;
	MCNUM mcnlsy = mcnsy;
	MCNUM mcnlsz = mcnsz;
	MCNUM mcnlp = mcnp;

	mcDEBUG_ENTER()
		mcDEBUG_STATE(
			mcnlx,
			mcnly,
			mcnlz,
			mcnlvx,
			mcnlvy,
			mcnlvz,
			mcnlt,
			mcnlsx,
			mcnlsy,
			mcnlsz,
			mcnlp)
#define mcabsorb mcabsorbAll
		/* TRACE Component Origin [1] */
		mccoordschange(mcposrOrigin, mcrotrOrigin,
			&mcnlx,
			&mcnly,
			&mcnlz,
			&mcnlvx,
			&mcnlvy,
			&mcnlvz,
			&mcnlsx,
			&mcnlsy,
			&mcnlsz);
	/* define label inside component Origin (without coords transformations) */
mcJumpTrace_Origin:
	SIG_MESSAGE("Origin (Trace)");
	mcDEBUG_COMP("Origin")
		mcDEBUG_STATE(
			mcnlx,
			mcnly,
			mcnlz,
			mcnlvx,
			mcnlvy,
			mcnlvz,
			mcnlt,
			mcnlsx,
			mcnlsy,
			mcnlsz,
			mcnlp)
#define x mcnlx
#define y mcnly
#define z mcnlz
#define vx mcnlvx
#define vy mcnlvy
#define vz mcnlvz
#define t mcnlt
#define sx mcnlsx
#define sy mcnlsy
#define sz mcnlsz
#define p mcnlp

#define mcabsorbComp mcabsorbCompOrigin
		STORE_NEUTRON(1,
			mcnlx,
			mcnly,
			mcnlz,
			mcnlvx,
			mcnlvy,
			mcnlvz,
			mcnlt,
			mcnlsx,
			mcnlsy,
			mcnlsz,
			mcnlp);
	mcScattered = 0;
	mcRestore = 0;
	mcNCounter[1]++;
	mcPCounter[1] += p;
	mcP2Counter[1] += p*p;
#define mccompcurname  Origin
#define mccompcurtype  Arm
#define mccompcurindex 1
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex
	/* Label for restoring  neutron */
	mcabsorbCompOrigin :
					   if (RESTORE) /* restore if needed */
					   {
						   RESTORE_NEUTRON(1,
							   mcnlx,
							   mcnly,
							   mcnlz,
							   mcnlvx,
							   mcnlvy,
							   mcnlvz,
							   mcnlt,
							   mcnlsx,
							   mcnlsy,
							   mcnlsz,
							   mcnlp);
					   }
#undef mcabsorbComp
#undef p
#undef sz
#undef sy
#undef sx
#undef t
#undef vz
#undef vy
#undef vx
#undef z
#undef y
#undef x
					   mcDEBUG_STATE(
						   mcnlx,
						   mcnly,
						   mcnlz,
						   mcnlvx,
						   mcnlvy,
						   mcnlvz,
						   mcnlt,
						   mcnlsx,
						   mcnlsy,
						   mcnlsz,
						   mcnlp)

						   /* TRACE Component Source [2] */
						   mccoordschange(mcposrSource, mcrotrSource,
							   &mcnlx,
							   &mcnly,
							   &mcnlz,
							   &mcnlvx,
							   &mcnlvy,
							   &mcnlvz,
							   &mcnlsx,
							   &mcnlsy,
							   &mcnlsz);
					   /* define label inside component Source (without coords transformations) */
				   mcJumpTrace_Source:
					   SIG_MESSAGE("Source (Trace)");
					   mcDEBUG_COMP("Source")
						   mcDEBUG_STATE(
							   mcnlx,
							   mcnly,
							   mcnlz,
							   mcnlvx,
							   mcnlvy,
							   mcnlvz,
							   mcnlt,
							   mcnlsx,
							   mcnlsy,
							   mcnlsz,
							   mcnlp)
#define x mcnlx
#define y mcnly
#define z mcnlz
#define vx mcnlvx
#define vy mcnlvy
#define vz mcnlvz
#define t mcnlt
#define sx mcnlsx
#define sy mcnlsy
#define sz mcnlsz
#define p mcnlp

#define mcabsorbComp mcabsorbCompSource
						   STORE_NEUTRON(2,
							   mcnlx,
							   mcnly,
							   mcnlz,
							   mcnlvx,
							   mcnlvy,
							   mcnlvz,
							   mcnlt,
							   mcnlsx,
							   mcnlsy,
							   mcnlsz,
							   mcnlp);
					   mcScattered = 0;
					   mcRestore = 0;
					   mcNCounter[2]++;
					   mcPCounter[2] += p;
					   mcP2Counter[2] += p*p;
#define mccompcurname  Source
#define mccompcurtype  Source_simple
#define mccompcurindex 2
#define pmul mccSource_pmul
#define square mccSource_square
#define srcArea mccSource_srcArea
					   {   /* Declarations of Source=Source_simple() SETTING parameters. */
						   MCNUM radius = mccSource_radius;
						   MCNUM yheight = mccSource_yheight;
						   MCNUM xwidth = mccSource_xwidth;
						   MCNUM dist = mccSource_dist;
						   MCNUM focus_xw = mccSource_focus_xw;
						   MCNUM focus_yh = mccSource_focus_yh;
						   MCNUM E0 = mccSource_E0;
						   MCNUM dE = mccSource_dE;
						   MCNUM lambda0 = mccSource_lambda0;
						   MCNUM dlambda = mccSource_dlambda;
						   MCNUM flux = mccSource_flux;
						   MCNUM gauss = mccSource_gauss;
						   int target_index = mccSource_target_index;
#line 127 "/usr/share/mcstas/2.3/sources/Source_simple.comp"
						   {
							   double chi, E, lambda, v, r, xf, yf, rf, dx, dy, pdir;

							   t = 0;
							   z = 0;

							   if (square == 1) {
								   x = xwidth * (rand01() - 0.5);
								   y = yheight * (rand01() - 0.5);
							   }
							   else {
								   chi = 2 * PI*rand01();                          /* Choose point on source */
								   r = sqrt(rand01())*radius;                    /* with uniform distribution. */
								   x = r*cos(chi);
								   y = r*sin(chi);
							   }
							   randvec_target_rect_real(&xf, &yf, &rf, &pdir,
								   0, 0, dist, focus_xw, focus_yh, ROT_A_CURRENT_COMP, x, y, z, 2);

							   dx = xf - x;
							   dy = yf - y;
							   rf = sqrt(dx*dx + dy*dy + dist*dist);

							   p = pdir*pmul;

							   if (lambda0 == 0) {
								   if (!gauss) {
									   E = E0 + dE*randpm1();              /*  Choose from uniform distribution */
								   }
								   else {
									   E = E0 + randnorm()*dE;
								   }
								   v = sqrt(E)*SE2V;
							   }
							   else {
								   if (!gauss) {
									   lambda = lambda0 + dlambda*randpm1();
								   }
								   else {
									   lambda = lambda0 + randnorm()*dlambda;
								   }
								   v = K2V*(2 * PI / lambda);
							   }

							   vz = v*dist / rf;
							   vy = v*dy / rf;
							   vx = v*dx / rf;
						   }
#line 6138 "/home/mcstas/test.c"
					   }   /* End of Source=Source_simple() SETTING parameter declarations. */
#undef srcArea
#undef square
#undef pmul
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex
						   /* Label for restoring  neutron */
					   mcabsorbCompSource :
										  if (RESTORE) /* restore if needed */
										  {
											  RESTORE_NEUTRON(2,
												  mcnlx,
												  mcnly,
												  mcnlz,
												  mcnlvx,
												  mcnlvy,
												  mcnlvz,
												  mcnlt,
												  mcnlsx,
												  mcnlsy,
												  mcnlsz,
												  mcnlp);
										  }
#undef mcabsorbComp
#undef p
#undef sz
#undef sy
#undef sx
#undef t
#undef vz
#undef vy
#undef vx
#undef z
#undef y
#undef x
										  mcDEBUG_STATE(
											  mcnlx,
											  mcnly,
											  mcnlz,
											  mcnlvx,
											  mcnlvy,
											  mcnlvz,
											  mcnlt,
											  mcnlsx,
											  mcnlsy,
											  mcnlsz,
											  mcnlp)

											  /* TRACE Component Emon [3] */
											  mccoordschange(mcposrEmon, mcrotrEmon,
												  &mcnlx,
												  &mcnly,
												  &mcnlz,
												  &mcnlvx,
												  &mcnlvy,
												  &mcnlvz,
												  &mcnlsx,
												  &mcnlsy,
												  &mcnlsz);
										  /* define label inside component Emon (without coords transformations) */
									  mcJumpTrace_Emon:
										  SIG_MESSAGE("Emon (Trace)");
										  mcDEBUG_COMP("Emon")
											  mcDEBUG_STATE(
												  mcnlx,
												  mcnly,
												  mcnlz,
												  mcnlvx,
												  mcnlvy,
												  mcnlvz,
												  mcnlt,
												  mcnlsx,
												  mcnlsy,
												  mcnlsz,
												  mcnlp)
#define x mcnlx
#define y mcnly
#define z mcnlz
#define vx mcnlvx
#define vy mcnlvy
#define vz mcnlvz
#define t mcnlt
#define sx mcnlsx
#define sy mcnlsy
#define sz mcnlsz
#define p mcnlp

#define mcabsorbComp mcabsorbCompEmon
											  STORE_NEUTRON(3,
												  mcnlx,
												  mcnly,
												  mcnlz,
												  mcnlvx,
												  mcnlvy,
												  mcnlvz,
												  mcnlt,
												  mcnlsx,
												  mcnlsy,
												  mcnlsz,
												  mcnlp);
										  mcScattered = 0;
										  mcRestore = 0;
										  mcNCounter[3]++;
										  mcPCounter[3] += p;
										  mcP2Counter[3] += p*p;
#define mccompcurname  Emon
#define mccompcurtype  E_monitor
#define mccompcurindex 3
#define nE mccEmon_nE
#define E_N mccEmon_E_N
#define E_p mccEmon_E_p
#define E_p2 mccEmon_E_p2
#define S_p mccEmon_S_p
#define S_pE mccEmon_S_pE
#define S_pE2 mccEmon_S_pE2
										  {   /* Declarations of Emon=E_monitor() SETTING parameters. */
											  char* filename = mccEmon_filename;
											  MCNUM xmin = mccEmon_xmin;
											  MCNUM xmax = mccEmon_xmax;
											  MCNUM ymin = mccEmon_ymin;
											  MCNUM ymax = mccEmon_ymax;
											  MCNUM xwidth = mccEmon_xwidth;
											  MCNUM yheight = mccEmon_yheight;
											  MCNUM Emin = mccEmon_Emin;
											  MCNUM Emax = mccEmon_Emax;
											  MCNUM restore_neutron = mccEmon_restore_neutron;
#line 90 "/usr/share/mcstas/2.3/monitors/E_monitor.comp"
											  {
												  int i;
												  double E;

												  PROP_Z0;
												  if (x>xmin && x<xmax && y>ymin && y<ymax)
												  {
													  E = VS2E*(vx*vx + vy*vy + vz*vz);

													  S_p += p;
													  S_pE += p*E;
													  S_pE2 += p*E*E;

													  i = floor((E - Emin)*nE / (Emax - Emin));
													  if (i >= 0 && i < nE)
													  {
														  E_N[i]++;
														  E_p[i] += p;
														  E_p2[i] += p*p;
														  SCATTER;
													  }
												  }
												  if (restore_neutron) {
													  RESTORE_NEUTRON(INDEX_CURRENT_COMP, x, y, z, vx, vy, vz, t, sx, sy, sz, p);
												  }
											  }
#line 6291 "/home/mcstas/test.c"
										  }   /* End of Emon=E_monitor() SETTING parameter declarations. */
#undef S_pE2
#undef S_pE
#undef S_p
#undef E_p2
#undef E_p
#undef E_N
#undef nE
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex
											  /* Label for restoring  neutron */
										  mcabsorbCompEmon :
														   if (RESTORE) /* restore if needed */
														   {
															   RESTORE_NEUTRON(3,
																   mcnlx,
																   mcnly,
																   mcnlz,
																   mcnlvx,
																   mcnlvy,
																   mcnlvz,
																   mcnlt,
																   mcnlsx,
																   mcnlsy,
																   mcnlsz,
																   mcnlp);
														   }
#undef mcabsorbComp
#undef p
#undef sz
#undef sy
#undef sx
#undef t
#undef vz
#undef vy
#undef vx
#undef z
#undef y
#undef x
														   mcDEBUG_STATE(
															   mcnlx,
															   mcnly,
															   mcnlz,
															   mcnlvx,
															   mcnlvy,
															   mcnlvz,
															   mcnlt,
															   mcnlsx,
															   mcnlsy,
															   mcnlsz,
															   mcnlp)

															   /* TRACE Component PSD [4] */
															   mccoordschange(mcposrPSD, mcrotrPSD,
																   &mcnlx,
																   &mcnly,
																   &mcnlz,
																   &mcnlvx,
																   &mcnlvy,
																   &mcnlvz,
																   &mcnlsx,
																   &mcnlsy,
																   &mcnlsz);
														   /* define label inside component PSD (without coords transformations) */
													   mcJumpTrace_PSD:
														   SIG_MESSAGE("PSD (Trace)");
														   mcDEBUG_COMP("PSD")
															   mcDEBUG_STATE(
																   mcnlx,
																   mcnly,
																   mcnlz,
																   mcnlvx,
																   mcnlvy,
																   mcnlvz,
																   mcnlt,
																   mcnlsx,
																   mcnlsy,
																   mcnlsz,
																   mcnlp)
#define x mcnlx
#define y mcnly
#define z mcnlz
#define vx mcnlvx
#define vy mcnlvy
#define vz mcnlvz
#define t mcnlt
#define sx mcnlsx
#define sy mcnlsy
#define sz mcnlsz
#define p mcnlp

#define mcabsorbComp mcabsorbCompPSD
															   STORE_NEUTRON(4,
																   mcnlx,
																   mcnly,
																   mcnlz,
																   mcnlvx,
																   mcnlvy,
																   mcnlvz,
																   mcnlt,
																   mcnlsx,
																   mcnlsy,
																   mcnlsz,
																   mcnlp);
														   mcScattered = 0;
														   mcRestore = 0;
														   mcNCounter[4]++;
														   mcPCounter[4] += p;
														   mcP2Counter[4] += p*p;
#define mccompcurname  PSD
#define mccompcurtype  PSD_monitor
#define mccompcurindex 4
#define nx mccPSD_nx
#define ny mccPSD_ny
#define PSD_N mccPSD_PSD_N
#define PSD_p mccPSD_PSD_p
#define PSD_p2 mccPSD_PSD_p2
														   {   /* Declarations of PSD=PSD_monitor() SETTING parameters. */
															   char* filename = mccPSD_filename;
															   MCNUM xmin = mccPSD_xmin;
															   MCNUM xmax = mccPSD_xmax;
															   MCNUM ymin = mccPSD_ymin;
															   MCNUM ymax = mccPSD_ymax;
															   MCNUM xwidth = mccPSD_xwidth;
															   MCNUM yheight = mccPSD_yheight;
															   MCNUM restore_neutron = mccPSD_restore_neutron;
#line 85 "/usr/share/mcstas/2.3/monitors/PSD_monitor.comp"
															   {
																   int i, j;

																   PROP_Z0;
																   if (x>xmin && x<xmax && y>ymin && y<ymax)
																   {
																	   i = floor((x - xmin)*nx / (xmax - xmin));
																	   j = floor((y - ymin)*ny / (ymax - ymin));
																	   PSD_N[i][j]++;
																	   PSD_p[i][j] += p;
																	   PSD_p2[i][j] += p*p;
																	   SCATTER;
																   }
																   if (restore_neutron) {
																	   RESTORE_NEUTRON(INDEX_CURRENT_COMP, x, y, z, vx, vy, vz, t, sx, sy, sz, p);
																   }
															   }
#line 6435 "/home/mcstas/test.c"
														   }   /* End of PSD=PSD_monitor() SETTING parameter declarations. */
#undef PSD_p2
#undef PSD_p
#undef PSD_N
#undef ny
#undef nx
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex
															   /* Label for restoring  neutron */
														   mcabsorbCompPSD :
																		   if (RESTORE) /* restore if needed */
																		   {
																			   RESTORE_NEUTRON(4,
																				   mcnlx,
																				   mcnly,
																				   mcnlz,
																				   mcnlvx,
																				   mcnlvy,
																				   mcnlvz,
																				   mcnlt,
																				   mcnlsx,
																				   mcnlsy,
																				   mcnlsz,
																				   mcnlp);
																		   }
#undef mcabsorbComp
#undef p
#undef sz
#undef sy
#undef sx
#undef t
#undef vz
#undef vy
#undef vx
#undef z
#undef y
#undef x
																		   mcDEBUG_STATE(
																			   mcnlx,
																			   mcnly,
																			   mcnlz,
																			   mcnlvx,
																			   mcnlvy,
																			   mcnlvz,
																			   mcnlt,
																			   mcnlsx,
																			   mcnlsy,
																			   mcnlsz,
																			   mcnlp)

																			   mcabsorbAll:
																		   mcDEBUG_LEAVE()
																			   mcDEBUG_STATE(
																				   mcnlx,
																				   mcnly,
																				   mcnlz,
																				   mcnlvx,
																				   mcnlvy,
																				   mcnlvz,
																				   mcnlt,
																				   mcnlsx,
																				   mcnlsy,
																				   mcnlsz,
																				   mcnlp)
																			   /* Copy neutron state to global variables. */
																			   mcnx = mcnlx;
																		   mcny = mcnly;
																		   mcnz = mcnlz;
																		   mcnvx = mcnlvx;
																		   mcnvy = mcnlvy;
																		   mcnvz = mcnlvz;
																		   mcnt = mcnlt;
																		   mcnsx = mcnlsx;
																		   mcnsy = mcnlsy;
																		   mcnsz = mcnlsz;
																		   mcnp = mcnlp;

} /* end trace */

void mcsave(FILE *handle) {
	if (!handle) mcsiminfo_init(NULL);
	/* User component SAVE code. */

	/* User SAVE code for component 'Emon'. */
	SIG_MESSAGE("Emon (Save)");
#define mccompcurname  Emon
#define mccompcurtype  E_monitor
#define mccompcurindex 3
#define nE mccEmon_nE
#define E_N mccEmon_E_N
#define E_p mccEmon_E_p
#define E_p2 mccEmon_E_p2
#define S_p mccEmon_S_p
#define S_pE mccEmon_S_pE
#define S_pE2 mccEmon_S_pE2
	{   /* Declarations of Emon=E_monitor() SETTING parameters. */
		char* filename = mccEmon_filename;
		MCNUM xmin = mccEmon_xmin;
		MCNUM xmax = mccEmon_xmax;
		MCNUM ymin = mccEmon_ymin;
		MCNUM ymax = mccEmon_ymax;
		MCNUM xwidth = mccEmon_xwidth;
		MCNUM yheight = mccEmon_yheight;
		MCNUM Emin = mccEmon_Emin;
		MCNUM Emax = mccEmon_Emax;
		MCNUM restore_neutron = mccEmon_restore_neutron;
#line 118 "/usr/share/mcstas/2.3/monitors/E_monitor.comp"
		{
			DETECTOR_OUT_1D(
				"Energy monitor",
				"Energy [meV]",
				"Intensity",
				"E", Emin, Emax, nE,
				&E_N[0], &E_p[0], &E_p2[0],
				filename);
			if (S_p) printf("<E> : %g meV , E-width : %g meV \n",
				S_pE / S_p, sqrt(S_pE2 / S_p - S_pE*S_pE / (S_p*S_p)));
		}
#line 6553 "/home/mcstas/test.c"
	}   /* End of Emon=E_monitor() SETTING parameter declarations. */
#undef S_pE2
#undef S_pE
#undef S_p
#undef E_p2
#undef E_p
#undef E_N
#undef nE
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		/* User SAVE code for component 'PSD'. */
	SIG_MESSAGE("PSD (Save)");
#define mccompcurname  PSD
#define mccompcurtype  PSD_monitor
#define mccompcurindex 4
#define nx mccPSD_nx
#define ny mccPSD_ny
#define PSD_N mccPSD_PSD_N
#define PSD_p mccPSD_PSD_p
#define PSD_p2 mccPSD_PSD_p2
	{   /* Declarations of PSD=PSD_monitor() SETTING parameters. */
		char* filename = mccPSD_filename;
		MCNUM xmin = mccPSD_xmin;
		MCNUM xmax = mccPSD_xmax;
		MCNUM ymin = mccPSD_ymin;
		MCNUM ymax = mccPSD_ymax;
		MCNUM xwidth = mccPSD_xwidth;
		MCNUM yheight = mccPSD_yheight;
		MCNUM restore_neutron = mccPSD_restore_neutron;
#line 103 "/usr/share/mcstas/2.3/monitors/PSD_monitor.comp"
		{
			DETECTOR_OUT_2D(
				"PSD monitor",
				"X position [cm]",
				"Y position [cm]",
				xmin*100.0, xmax*100.0, ymin*100.0, ymax*100.0,
				nx, ny,
				&PSD_N[0][0], &PSD_p[0][0], &PSD_p2[0][0],
				filename);
		}
#line 6596 "/home/mcstas/test.c"
	}   /* End of PSD=PSD_monitor() SETTING parameter declarations. */
#undef PSD_p2
#undef PSD_p
#undef PSD_N
#undef ny
#undef nx
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

	if (!handle) mcsiminfo_close();
} /* end save */
void mcfinally(void) {
	/* User component FINALLY code. */
	mcsiminfo_init(NULL);
	mcsave(mcsiminfo_file); /* save data when simulation ends */

	if (!mcNCounter[1]) fprintf(stderr, "Warning: No neutron could reach Component[1] Origin\n");
	if (mcAbsorbProp[1]) fprintf(stderr, "Warning: %g events were removed in Component[1] Origin=Arm()\n"
		"         (negative time, miss next components, rounding errors, Nan, Inf).\n", mcAbsorbProp[1]);
	if (!mcNCounter[2]) fprintf(stderr, "Warning: No neutron could reach Component[2] Source\n");
	if (mcAbsorbProp[2]) fprintf(stderr, "Warning: %g events were removed in Component[2] Source=Source_simple()\n"
		"         (negative time, miss next components, rounding errors, Nan, Inf).\n", mcAbsorbProp[2]);
	if (!mcNCounter[3]) fprintf(stderr, "Warning: No neutron could reach Component[3] Emon\n");
	if (mcAbsorbProp[3]) fprintf(stderr, "Warning: %g events were removed in Component[3] Emon=E_monitor()\n"
		"         (negative time, miss next components, rounding errors, Nan, Inf).\n", mcAbsorbProp[3]);
	if (!mcNCounter[4]) fprintf(stderr, "Warning: No neutron could reach Component[4] PSD\n");
	if (mcAbsorbProp[4]) fprintf(stderr, "Warning: %g events were removed in Component[4] PSD=PSD_monitor()\n"
		"         (negative time, miss next components, rounding errors, Nan, Inf).\n", mcAbsorbProp[4]);
	mcsiminfo_close();
} /* end finally */
#define magnify mcdis_magnify
#define line mcdis_line
#define dashed_line mcdis_dashed_line
#define multiline mcdis_multiline
#define rectangle mcdis_rectangle
#define box mcdis_box
#define circle mcdis_circle
void mcdisplay(void) {
	printf("MCDISPLAY: start\n");
	/* Components MCDISPLAY code. */

	/* MCDISPLAY code for component 'Origin'. */
	SIG_MESSAGE("Origin (McDisplay)");
	printf("MCDISPLAY: component %s\n", "Origin");
#define mccompcurname  Origin
#define mccompcurtype  Arm
#define mccompcurindex 1
#line 42 "/usr/share/mcstas/2.3/optics/Arm.comp"
	{
		/* A bit ugly; hard-coded dimensions. */
		magnify("");
		line(0, 0, 0, 0.2, 0, 0);
		line(0, 0, 0, 0, 0.2, 0);
		line(0, 0, 0, 0, 0, 0.2);
	}
#line 6649 "/home/mcstas/test.c"
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

	/* MCDISPLAY code for component 'Source'. */
	SIG_MESSAGE("Source (McDisplay)");
	printf("MCDISPLAY: component %s\n", "Source");
#define mccompcurname  Source
#define mccompcurtype  Source_simple
#define mccompcurindex 2
#define pmul mccSource_pmul
#define square mccSource_square
#define srcArea mccSource_srcArea
	{   /* Declarations of Source=Source_simple() SETTING parameters. */
		MCNUM radius = mccSource_radius;
		MCNUM yheight = mccSource_yheight;
		MCNUM xwidth = mccSource_xwidth;
		MCNUM dist = mccSource_dist;
		MCNUM focus_xw = mccSource_focus_xw;
		MCNUM focus_yh = mccSource_focus_yh;
		MCNUM E0 = mccSource_E0;
		MCNUM dE = mccSource_dE;
		MCNUM lambda0 = mccSource_lambda0;
		MCNUM dlambda = mccSource_dlambda;
		MCNUM flux = mccSource_flux;
		MCNUM gauss = mccSource_gauss;
		int target_index = mccSource_target_index;
#line 173 "/usr/share/mcstas/2.3/sources/Source_simple.comp"
		{
			if (square == 1) {
				magnify("xy");
				rectangle("xy", 0, 0, 0, xwidth, yheight);
			}
			else {
				magnify("xy");
				circle("xy", 0, 0, 0, radius);
			}
			if (dist) {
				dashed_line(0, 0, 0, -focus_xw / 2, -focus_yh / 2, dist, 4);
				dashed_line(0, 0, 0, focus_xw / 2, -focus_yh / 2, dist, 4);
				dashed_line(0, 0, 0, focus_xw / 2, focus_yh / 2, dist, 4);
				dashed_line(0, 0, 0, -focus_xw / 2, focus_yh / 2, dist, 4);
			}
		}
#line 6693 "/home/mcstas/test.c"
	}   /* End of Source=Source_simple() SETTING parameter declarations. */
#undef srcArea
#undef square
#undef pmul
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		/* MCDISPLAY code for component 'Emon'. */
	SIG_MESSAGE("Emon (McDisplay)");
	printf("MCDISPLAY: component %s\n", "Emon");
#define mccompcurname  Emon
#define mccompcurtype  E_monitor
#define mccompcurindex 3
#define nE mccEmon_nE
#define E_N mccEmon_E_N
#define E_p mccEmon_E_p
#define E_p2 mccEmon_E_p2
#define S_p mccEmon_S_p
#define S_pE mccEmon_S_pE
#define S_pE2 mccEmon_S_pE2
	{   /* Declarations of Emon=E_monitor() SETTING parameters. */
		char* filename = mccEmon_filename;
		MCNUM xmin = mccEmon_xmin;
		MCNUM xmax = mccEmon_xmax;
		MCNUM ymin = mccEmon_ymin;
		MCNUM ymax = mccEmon_ymax;
		MCNUM xwidth = mccEmon_xwidth;
		MCNUM yheight = mccEmon_yheight;
		MCNUM Emin = mccEmon_Emin;
		MCNUM Emax = mccEmon_Emax;
		MCNUM restore_neutron = mccEmon_restore_neutron;
#line 131 "/usr/share/mcstas/2.3/monitors/E_monitor.comp"
		{
			magnify("xy");
			multiline(5, (double)xmin, (double)ymin, 0.0,
				(double)xmax, (double)ymin, 0.0,
				(double)xmax, (double)ymax, 0.0,
				(double)xmin, (double)ymax, 0.0,
				(double)xmin, (double)ymin, 0.0);
		}
#line 6735 "/home/mcstas/test.c"
	}   /* End of Emon=E_monitor() SETTING parameter declarations. */
#undef S_pE2
#undef S_pE
#undef S_p
#undef E_p2
#undef E_p
#undef E_N
#undef nE
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

		/* MCDISPLAY code for component 'PSD'. */
	SIG_MESSAGE("PSD (McDisplay)");
	printf("MCDISPLAY: component %s\n", "PSD");
#define mccompcurname  PSD
#define mccompcurtype  PSD_monitor
#define mccompcurindex 4
#define nx mccPSD_nx
#define ny mccPSD_ny
#define PSD_N mccPSD_PSD_N
#define PSD_p mccPSD_PSD_p
#define PSD_p2 mccPSD_PSD_p2
	{   /* Declarations of PSD=PSD_monitor() SETTING parameters. */
		char* filename = mccPSD_filename;
		MCNUM xmin = mccPSD_xmin;
		MCNUM xmax = mccPSD_xmax;
		MCNUM ymin = mccPSD_ymin;
		MCNUM ymax = mccPSD_ymax;
		MCNUM xwidth = mccPSD_xwidth;
		MCNUM yheight = mccPSD_yheight;
		MCNUM restore_neutron = mccPSD_restore_neutron;
#line 115 "/usr/share/mcstas/2.3/monitors/PSD_monitor.comp"
		{
			magnify("xy");
			multiline(5, (double)xmin, (double)ymin, 0.0,
				(double)xmax, (double)ymin, 0.0,
				(double)xmax, (double)ymax, 0.0,
				(double)xmin, (double)ymax, 0.0,
				(double)xmin, (double)ymin, 0.0);
		}
#line 6777 "/home/mcstas/test.c"
	}   /* End of PSD=PSD_monitor() SETTING parameter declarations. */
#undef PSD_p2
#undef PSD_p
#undef PSD_N
#undef ny
#undef nx
#undef mccompcurname
#undef mccompcurtype
#undef mccompcurindex

	printf("MCDISPLAY: end\n");
} /* end display */
#undef magnify
#undef line
#undef dashed_line
#undef multiline
#undef rectangle
#undef box
#undef circle
  /* end of generated C code /home/mcstas/test.c */