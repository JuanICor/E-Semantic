#define _ idc()
int idc(void);
int idc_or(void);

#define OR_pattern  if(idc_or())
#define OR else if (idc_or())