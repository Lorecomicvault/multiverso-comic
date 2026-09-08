import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setPixelFormat('yuv420p');
Config.setCodec('h264');
Config.setConcurrency(2);
Config.setOverwriteOutput(true);
Config.setChromiumHeadlessMode(true);
Config.setChromiumMultiProcessOnLinux(true);
Config.setChromiumDisableWebSecurity(true);
Config.setTimeoutInMilliseconds(120000);
