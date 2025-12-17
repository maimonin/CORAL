attackGoal(vulnerablePod(Pod)).

hacl('Internet', frontend, 'HTTP', '80').

dataFlow(frontend, adservice, 'TCP', '8080').
dataFlow(frontend, cartservice, 'TCP', '8080').
dataFlow(frontend, checkoutservice, 'TCP', '8080').
dataFlow(frontend, currencyservice, 'TCP', '8080').
dataFlow(frontend, productcatalogservice, 'TCP', '8080').
dataFlow(frontend, recommendationservice, 'TCP', '8080').
dataFlow(frontend, shippingservice, 'TCP', '8080').
dataFlow(cartservice, redis_cart, 'TCP', '7070').
dataFlow(checkoutservice, cartservice, 'TCP', '5050').
dataFlow(checkoutservice, currencyservice, 'TCP', '5050').
dataFlow(checkoutservice, emailservice, 'TCP', '5050').
dataFlow(checkoutservice, paymentservice, 'TCP', '5050').
dataFlow(checkoutservice, productcatalogservice, 'TCP', '5050').
dataFlow(checkoutservice, shippingservice, 'TCP', '5050').
dataFlow(recommendationservice, productcatalogservice, 'TCP', '8080').

residesOn(adservice, 'expat', '2_4_8_r0').
vulExists('CVE-2022-40674', 'expat', '2_4_8_r0', 'Network', 'CIA_loss', 'CRITICAL').
residesOn(adservice, 'expat', '2_4_8_r0').
vulExists('CVE-2022-43680', 'expat', '2_4_8_r0', 'Network', 'A_loss', 'HIGH').
residesOn(cartservice, 'krb5_libs', '1_19_3_r0').
vulExists('CVE-2022-42898', 'krb5_libs', '1_19_3_r0', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'apt', '2_2_4').
vulExists('CVE-2011-3374', 'apt', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'bash', '5_1_2+deb11u1').
vulExists('CVE-2022-3715', 'bash', '5_1_2+deb11u1', 'Local', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'bsdutils', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'bsdutils', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'coreutils', '8_32_4').
vulExists('CVE-2016-2781', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'coreutils', '8_32_4').
vulExists('CVE-2017-18018', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'e2fsprogs', '1_46_2_2').
vulExists('CVE-2022-1304', 'e2fsprogs', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'libapt_pkg6_0', '2_2_4').
vulExists('CVE-2011-3374', 'libapt_pkg6_0', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'libblkid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libblkid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2010-4756', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2018-20796', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010022', 'libc_bin', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010023', 'libc_bin', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010024', 'libc_bin', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010025', 'libc_bin', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-9192', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2010-4756', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2018-20796', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010022', 'libc6', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010023', 'libc6', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010024', 'libc6', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010025', 'libc6', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-9192', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libcom_err2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libcom_err2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'libdb5_3', '5_3_28+dfsg1_0_8').
vulExists('CVE-2019-8457', 'libdb5_3', '5_3_28+dfsg1_0_8', 'Network', 'CIA_loss', 'CRITICAL').
residesOn(emailservice, 'libexpat1', '2_2_10_2+deb11u4').
vulExists('CVE-2022-43680', 'libexpat1', '2_2_10_2+deb11u4', 'Network', 'A_loss', 'HIGH').
residesOn(emailservice, 'libexpat1', '2_2_10_2+deb11u4').
vulExists('CVE-2013-0340', 'libexpat1', '2_2_10_2+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libext2fs2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libext2fs2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2021-33560', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'HIGH').
residesOn(emailservice, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2018-6829', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libgnutls30', '3_7_1_5+deb11u2').
vulExists('CVE-2011-3389', 'libgnutls30', '3_7_1_5+deb11u2', 'Network', 'C_loss', 'LOW').
residesOn(emailservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libk5crypto3', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libk5crypto3', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libk5crypto3', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libkrb5_3', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libkrb5_3', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libkrb5_3', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libkrb5support0', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(emailservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libkrb5support0', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libkrb5support0', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'libmount1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libmount1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libncursesw6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libncursesw6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-11164', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-16231', 'libpcre3', '2_8_39_13', 'Local', 'A_loss', 'LOW').
residesOn(emailservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7245', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7246', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2019-20838', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36084', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36085', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36086', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36087', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice, 'libsmartcols1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libsmartcols1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-45346', 'libsqlite3_0', '3_34_1_3', 'Network', 'C_loss', 'MEDIUM').
residesOn(emailservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-36690', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2022-35737', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(emailservice, 'libss2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libss2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(emailservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(emailservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'libssl1_1', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(emailservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(emailservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libsystemd0', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(emailservice, 'libtasn1_6', '4_16_0_2').
vulExists('CVE-2021-46848', 'libtasn1_6', '4_16_0_2', 'Network', 'CA_loss', 'CRITICAL').
residesOn(emailservice, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libtinfo6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libtinfo6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libudev1', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(emailservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libudev1', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(emailservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libudev1', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(emailservice, 'libuuid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libuuid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'login', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'login', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'login', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'login', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'login', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'login', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice, 'logsave', '1_46_2_2').
vulExists('CVE-2022-1304', 'logsave', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'mount', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'mount', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_base', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_base', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_bin', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_bin', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(emailservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(emailservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'openssl', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'passwd', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'passwd', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(emailservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'passwd', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2020-16156', 'perl_base', '5_32_1_4+deb11u2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2011-4116', 'perl_base', '5_32_1_4+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice, 'tar', '1_34+dfsg_1').
vulExists('CVE-2005-2541', 'tar', '1_34+dfsg_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice, 'util_linux', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'util_linux', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(frontend, 'krb5_libs', '1_19_3_r0').
vulExists('CVE-2022-42898', 'krb5_libs', '1_19_3_r0', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(frontend, 'libxml2', '2_9_14_r1').
vulExists('CVE-2022-40303', 'libxml2', '2_9_14_r1', 'Network', 'A_loss', 'HIGH').
residesOn(frontend, 'libxml2', '2_9_14_r1').
vulExists('CVE-2022-40304', 'libxml2', '2_9_14_r1', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'apt', '2_2_4').
vulExists('CVE-2011-3374', 'apt', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'bash', '5_1_2+deb11u1').
vulExists('CVE-2022-3715', 'bash', '5_1_2+deb11u1', 'Local', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice, 'bsdutils', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'bsdutils', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'coreutils', '8_32_4').
vulExists('CVE-2016-2781', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'coreutils', '8_32_4').
vulExists('CVE-2017-18018', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'e2fsprogs', '1_46_2_2').
vulExists('CVE-2022-1304', 'e2fsprogs', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'libapt_pkg6_0', '2_2_4').
vulExists('CVE-2011-3374', 'libapt_pkg6_0', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libblkid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libblkid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2010-4756', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2018-20796', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010022', 'libc_bin', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010023', 'libc_bin', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010024', 'libc_bin', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-1010025', 'libc_bin', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libc_bin', '2_31_13+deb11u4').
vulExists('CVE-2019-9192', 'libc_bin', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2010-4756', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2018-20796', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010022', 'libc6', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010023', 'libc6', '2_31_13+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010024', 'libc6', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-1010025', 'libc6', '2_31_13+deb11u4', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libc6', '2_31_13+deb11u4').
vulExists('CVE-2019-9192', 'libc6', '2_31_13+deb11u4', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libcom_err2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libcom_err2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'libdb5_3', '5_3_28+dfsg1_0_8').
vulExists('CVE-2019-8457', 'libdb5_3', '5_3_28+dfsg1_0_8', 'Network', 'CIA_loss', 'CRITICAL').
residesOn(recommendationservice, 'libexpat1', '2_2_10_2+deb11u4').
vulExists('CVE-2022-43680', 'libexpat1', '2_2_10_2+deb11u4', 'Network', 'A_loss', 'HIGH').
residesOn(recommendationservice, 'libexpat1', '2_2_10_2+deb11u4').
vulExists('CVE-2013-0340', 'libexpat1', '2_2_10_2+deb11u4', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libext2fs2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libext2fs2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2021-33560', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'HIGH').
residesOn(recommendationservice, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2018-6829', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libgnutls30', '3_7_1_5+deb11u2').
vulExists('CVE-2011-3389', 'libgnutls30', '3_7_1_5+deb11u2', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libgssapi_krb5_2', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libgssapi_krb5_2', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libk5crypto3', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libk5crypto3', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libk5crypto3', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libk5crypto3', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libkrb5_3', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libkrb5_3', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libkrb5_3', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libkrb5_3', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2022-42898', 'libkrb5support0', '1_18_3_6+deb11u2', 'Network', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2004-0971', 'libkrb5support0', '1_18_3_6+deb11u2', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libkrb5support0', '1_18_3_6+deb11u2').
vulExists('CVE-2018-5709', 'libkrb5support0', '1_18_3_6+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'libmount1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libmount1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libncursesw6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libncursesw6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-11164', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-16231', 'libpcre3', '2_8_39_13', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7245', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7246', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libpcre3', '2_8_39_13').
vulExists('CVE-2019-20838', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36084', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36085', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36086', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36087', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsmartcols1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libsmartcols1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-45346', 'libsqlite3_0', '3_34_1_3', 'Network', 'C_loss', 'MEDIUM').
residesOn(recommendationservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-36690', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2022-35737', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libss2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libss2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(recommendationservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(recommendationservice, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'libssl1_1', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(recommendationservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(recommendationservice, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libsystemd0', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libtasn1_6', '4_16_0_2').
vulExists('CVE-2021-46848', 'libtasn1_6', '4_16_0_2', 'Network', 'CA_loss', 'CRITICAL').
residesOn(recommendationservice, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libtinfo6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libtinfo6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libudev1', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(recommendationservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libudev1', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(recommendationservice, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libudev1', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(recommendationservice, 'libuuid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libuuid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'login', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'login', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'login', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'login', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'login', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'login', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'logsave', '1_46_2_2').
vulExists('CVE-2022-1304', 'logsave', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'mount', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'mount', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_base', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_base', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_bin', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_bin', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(recommendationservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(recommendationservice, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'openssl', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'passwd', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'passwd', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice, 'passwd', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'passwd', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2020-16156', 'perl_base', '5_32_1_4+deb11u2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2011-4116', 'perl_base', '5_32_1_4+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice, 'tar', '1_34+dfsg_1').
vulExists('CVE-2005-2541', 'tar', '1_34+dfsg_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice, 'util_linux', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'util_linux', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
