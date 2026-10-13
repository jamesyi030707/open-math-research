#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
/* Independent bounded exact scan. Reads independently computed q cutoffs.
   Explicitly guards every intermediate integer operation; stops at 1 because
   all later values are <=2 and initial n>=3. */
int main(int argc,char**argv){
 unsigned cutoff[301]; FILE*f=fopen(argv[1],"r");if(!f)return 1;
 for(int j=1;j<=300;j++)if(fscanf(f,"%u",cutoff+j)!=1)return 2;fclose(f);
 uint64_t peak=0,steps=0;unsigned hits=0;
 for(uint64_t n=3;n<=4076810;n++){
  uint64_t x=n;unsigned q=0;
  for(int j=1;j<=300 && x!=1;j++){
   if(x&1){ if(x>(UINT64_MAX-1)/3){fprintf(stderr,"OVERFLOW\n");return 3;} x=(x*3+1)>>1; q++;}else x>>=1;
   steps++;if(x>peak)peak=x;
   if(q<=cutoff[j] && x>=n){printf("%" PRIu64 " %d %u\n",n,j,q);hits++;}
  }
 }
 fprintf(stderr,"scan n=3..4076810, j<=300, hits=%u, steps=%" PRIu64 ", peak=%" PRIu64 ", overflow=0\n",hits,steps,peak);
}
