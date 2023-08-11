#ifndef CUSTOM_SERIAL_COM_H_
#define CUSTOM_SERIAL_COM_H_

#define CSC_CMD_READ_PI  2
#define CSC_CMD_WRITE_PI_ERROR  3
#define CSC_CMD_WRITE_PI_LOG    4
#define CSC_CMD_WRITE_PI_STATUS 5
#define CSC_CMD_WRITE_PI_AUDIO  6

int csc_wait_on_pi();
int csc_read_data(byte* databuf);
int csc_write_data(int data_type, byte* databuf, int num_bytes);

#endif
