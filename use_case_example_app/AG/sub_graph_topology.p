attackGoal(vulnerablePod(Pod)).

dataFlow(cartservice, redis_cart, 'TCP', '7070').
dataFlow(frontend_3, adservice_0, 'TCP', '13979').
dataFlow(frontend_3, productcatalogservice_0, 'TCP', '13979').
dataFlow(frontend_3, cartservice, 'TCP', '13979').
dataFlow(frontend_3, recommendationservice_1, 'TCP', '13979').
dataFlow(frontend_3, shippingservice_1, 'TCP', '13979').
dataFlow(frontend_3, checkoutservice_0, 'TCP', '13979').
dataFlow(recommendationservice_1, productcatalogservice_0, 'TCP', '31365').
dataFlow(checkoutservice_0, productcatalogservice_1, 'TCP', '14905').
dataFlow(checkoutservice_0, cartservice, 'TCP', '14905').
dataFlow(checkoutservice_0, currencyservice_1, 'TCP', '14905').
dataFlow(checkoutservice_0, emailservice_1, 'TCP', '14905').
dataFlow(checkoutservice_0, paymentservice_1, 'TCP', '14905').
dataFlow(checkoutservice_0, shippingservice_1, 'TCP', '14905').
hacl('Internet', frontend_3, 'HTTP', '80').

residesOn(adservice_0, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(adservice_0, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(adservice_0, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(productcatalogservice_0, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(productcatalogservice_0, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(productcatalogservice_0, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(productcatalogservice_1, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(productcatalogservice_1, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(productcatalogservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(currencyservice_1, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(currencyservice_1, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(currencyservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(emailservice_1, 'apt', '2_2_4').
vulExists('CVE-2011-3374', 'apt', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'bash', '5_1_2+deb11u1').
vulExists('CVE-2022-3715', 'bash', '5_1_2+deb11u1', 'Local', 'CIA_loss', 'MEDIUM').
residesOn(emailservice_1, 'bsdutils', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'bsdutils', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'coreutils', '8_32_4').
vulExists('CVE-2016-2781', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'coreutils', '8_32_4').
vulExists('CVE-2017-18018', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'e2fsprogs', '1_46_2_2').
vulExists('CVE-2022-1304', 'e2fsprogs', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'libapt_pkg6_0', '2_2_4').
vulExists('CVE-2011-3374', 'libapt_pkg6_0', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libblkid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libblkid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2010-4756', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2018-20796', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010022', 'libc_bin', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010023', 'libc_bin', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010024', 'libc_bin', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010025', 'libc_bin', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-9192', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2010-4756', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2018-20796', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010022', 'libc6', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010023', 'libc6', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010024', 'libc6', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010025', 'libc6', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-9192', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libcom_err2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libcom_err2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'libdb5_3', '5_3_28+dfsg1_0_8').
vulExists('CVE-2019-8457', 'libdb5_3', '5_3_28+dfsg1_0_8', 'Network', 'CIA_loss', 'CRITICAL').
residesOn(emailservice_1, 'libexpat1', '2_2_10_2+deb11u5').
vulExists('CVE-2013-0340', 'libexpat1', '2_2_10_2+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libext2fs2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libext2fs2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2021-33560', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'HIGH').
residesOn(emailservice_1, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2018-6829', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libgnutls30', '3_7_1_5+deb11u2').
vulExists('CVE-2011-3389', 'libgnutls30', '3_7_1_5+deb11u2', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libgssapi_krb5_2', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libgssapi_krb5_2', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libgssapi_krb5_2', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libgssapi_krb5_2', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libk5crypto3', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libk5crypto3', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libk5crypto3', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libk5crypto3', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libkrb5_3', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libkrb5_3', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libkrb5_3', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libkrb5_3', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libkrb5support0', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libkrb5support0', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libkrb5support0', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libkrb5support0', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'libmount1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libmount1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libncursesw6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice_1, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libncursesw6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-11164', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-16231', 'libpcre3', '2_8_39_13', 'Local', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7245', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7246', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2019-20838', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36084', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36085', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36086', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36087', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsmartcols1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libsmartcols1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-36690', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-45346', 'libsqlite3_0', '3_34_1_3', 'Network', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2022-35737', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libss2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libss2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(emailservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(emailservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'libssl1_1', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(emailservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-4415', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'C_loss', 'MEDIUM').
residesOn(emailservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(emailservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libsystemd0', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libtasn1_6', '4_16_0_2').
vulExists('CVE-2021-46848', 'libtasn1_6', '4_16_0_2', 'Network', 'CA_loss', 'CRITICAL').
residesOn(emailservice_1, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libtinfo6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice_1, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libtinfo6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libudev1', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(emailservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-4415', 'libudev1', '247_3_7+deb11u1', 'Local', 'C_loss', 'MEDIUM').
residesOn(emailservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libudev1', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(emailservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libudev1', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(emailservice_1, 'libuuid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libuuid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'login', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'login', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'login', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'logsave', '1_46_2_2').
vulExists('CVE-2022-1304', 'logsave', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'mount', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'mount', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_base', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice_1, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_base', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_bin', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(emailservice_1, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_bin', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(emailservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(emailservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'openssl', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'passwd', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'passwd', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(emailservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'passwd', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2020-16156', 'perl_base', '5_32_1_4+deb11u2', 'Local', 'CIA_loss', 'HIGH').
residesOn(emailservice_1, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2011-4116', 'perl_base', '5_32_1_4+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(emailservice_1, 'tar', '1_34+dfsg_1').
vulExists('CVE-2005-2541', 'tar', '1_34+dfsg_1', 'Local', 'CIA_loss', 'LOW').
residesOn(emailservice_1, 'util_linux', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'util_linux', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(emailservice_1, 'setuptools', '63_2_0').
vulExists('CVE-2022-40897', 'setuptools', '63_2_0', 'Network', 'A_loss', 'HIGH').
residesOn(emailservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(paymentservice_1, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(paymentservice_1, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(paymentservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'apt', '2_2_4').
vulExists('CVE-2011-3374', 'apt', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'bash', '5_1_2+deb11u1').
vulExists('CVE-2022-3715', 'bash', '5_1_2+deb11u1', 'Local', 'CIA_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'bsdutils', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'bsdutils', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'coreutils', '8_32_4').
vulExists('CVE-2016-2781', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'coreutils', '8_32_4').
vulExists('CVE-2017-18018', 'coreutils', '8_32_4', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'e2fsprogs', '1_46_2_2').
vulExists('CVE-2022-1304', 'e2fsprogs', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libapt_pkg6_0', '2_2_4').
vulExists('CVE-2011-3374', 'libapt_pkg6_0', '2_2_4', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libblkid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libblkid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2010-4756', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2018-20796', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010022', 'libc_bin', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010023', 'libc_bin', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010024', 'libc_bin', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-1010025', 'libc_bin', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libc_bin', '2_31_13+deb11u5').
vulExists('CVE-2019-9192', 'libc_bin', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2010-4756', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2018-20796', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010022', 'libc6', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010023', 'libc6', '2_31_13+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010024', 'libc6', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-1010025', 'libc6', '2_31_13+deb11u5', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libc6', '2_31_13+deb11u5').
vulExists('CVE-2019-9192', 'libc6', '2_31_13+deb11u5', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libcom_err2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libcom_err2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libdb5_3', '5_3_28+dfsg1_0_8').
vulExists('CVE-2019-8457', 'libdb5_3', '5_3_28+dfsg1_0_8', 'Network', 'CIA_loss', 'CRITICAL').
residesOn(recommendationservice_1, 'libexpat1', '2_2_10_2+deb11u5').
vulExists('CVE-2013-0340', 'libexpat1', '2_2_10_2+deb11u5', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libext2fs2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libext2fs2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2021-33560', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'HIGH').
residesOn(recommendationservice_1, 'libgcrypt20', '1_8_7_6').
vulExists('CVE-2018-6829', 'libgcrypt20', '1_8_7_6', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libgnutls30', '3_7_1_5+deb11u2').
vulExists('CVE-2011-3389', 'libgnutls30', '3_7_1_5+deb11u2', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libgssapi_krb5_2', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libgssapi_krb5_2', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libgssapi_krb5_2', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libgssapi_krb5_2', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libk5crypto3', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libk5crypto3', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libk5crypto3', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libk5crypto3', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libkrb5_3', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libkrb5_3', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libkrb5_3', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libkrb5_3', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libkrb5support0', '1_18_3_6+deb11u3').
vulExists('CVE-2004-0971', 'libkrb5support0', '1_18_3_6+deb11u3', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libkrb5support0', '1_18_3_6+deb11u3').
vulExists('CVE-2018-5709', 'libkrb5support0', '1_18_3_6+deb11u3', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'libmount1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libmount1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libncursesw6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libncursesw6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libncursesw6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-11164', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-16231', 'libpcre3', '2_8_39_13', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7245', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2017-7246', 'libpcre3', '2_8_39_13', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libpcre3', '2_8_39_13').
vulExists('CVE-2019-20838', 'libpcre3', '2_8_39_13', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36084', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36085', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36086', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsepol1', '3_1_1').
vulExists('CVE-2021-36087', 'libsepol1', '3_1_1', 'Local', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsmartcols1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libsmartcols1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-36690', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2021-45346', 'libsqlite3_0', '3_34_1_3', 'Network', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libsqlite3_0', '3_34_1_3').
vulExists('CVE-2022-35737', 'libsqlite3_0', '3_34_1_3', 'Network', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libss2', '1_46_2_2').
vulExists('CVE-2022-1304', 'libss2', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'libssl1_1', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(recommendationservice_1, 'libssl1_1', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'libssl1_1', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2022-4415', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'C_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libsystemd0', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(recommendationservice_1, 'libsystemd0', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libsystemd0', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libtasn1_6', '4_16_0_2').
vulExists('CVE-2021-46848', 'libtasn1_6', '4_16_0_2', 'Network', 'CA_loss', 'CRITICAL').
residesOn(recommendationservice_1, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'libtinfo6', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice_1, 'libtinfo6', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'libtinfo6', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-3821', 'libudev1', '247_3_7+deb11u1', 'Local', 'A_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2022-4415', 'libudev1', '247_3_7+deb11u1', 'Local', 'C_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2013-4392', 'libudev1', '247_3_7+deb11u1', 'Local', 'CI_loss', 'LOW').
residesOn(recommendationservice_1, 'libudev1', '247_3_7+deb11u1').
vulExists('CVE-2020-13529', 'libudev1', '247_3_7+deb11u1', 'AdjacentNetwork', 'A_loss', 'LOW').
residesOn(recommendationservice_1, 'libuuid1', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'libuuid1', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'login', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'login', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'login', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'login', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'logsave', '1_46_2_2').
vulExists('CVE-2022-1304', 'logsave', '1_46_2_2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'mount', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'mount', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_base', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice_1, 'ncurses_base', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_base', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2022-29458', 'ncurses_bin', '6_2+20201114_2', 'Local', 'CA_loss', 'HIGH').
residesOn(recommendationservice_1, 'ncurses_bin', '6_2+20201114_2').
vulExists('CVE-2021-39537', 'ncurses_bin', '6_2+20201114_2', 'Network', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2022-2097', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'C_loss', 'MEDIUM').
residesOn(recommendationservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2007-6755', 'openssl', '1_1_1n_0+deb11u3', 'Network', 'CI_loss', 'LOW').
residesOn(recommendationservice_1, 'openssl', '1_1_1n_0+deb11u3').
vulExists('CVE-2010-0928', 'openssl', '1_1_1n_0+deb11u3', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2007-5686', 'passwd', '1_4_8_1_1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2013-4235', 'passwd', '1_4_8_1_1', 'Local', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'passwd', '1_4_8_1_1').
vulExists('CVE-2019-19882', 'passwd', '1_4_8_1_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2020-16156', 'perl_base', '5_32_1_4+deb11u2', 'Local', 'CIA_loss', 'HIGH').
residesOn(recommendationservice_1, 'perl_base', '5_32_1_4+deb11u2').
vulExists('CVE-2011-4116', 'perl_base', '5_32_1_4+deb11u2', 'Network', 'I_loss', 'LOW').
residesOn(recommendationservice_1, 'tar', '1_34+dfsg_1').
vulExists('CVE-2005-2541', 'tar', '1_34+dfsg_1', 'Local', 'CIA_loss', 'LOW').
residesOn(recommendationservice_1, 'util_linux', '2_36_1_8+deb11u1').
vulExists('CVE-2022-0563', 'util_linux', '2_36_1_8+deb11u1', 'Local', 'C_loss', 'LOW').
residesOn(recommendationservice_1, 'setuptools', '63_2_0').
vulExists('CVE-2022-40897', 'setuptools', '63_2_0', 'Network', 'A_loss', 'HIGH').
residesOn(recommendationservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(shippingservice_1, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(shippingservice_1, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(shippingservice_1, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(checkoutservice_0, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(checkoutservice_0, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(checkoutservice_0, 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c').
vulExists('CVE-2022-41717', 'golang_org_x_net', 'v0_0_0_20220906165146_f3363e06e74c', 'Network', 'A_loss', 'MEDIUM').
residesOn(frontend_3, 'libcrypto3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libcrypto3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
residesOn(frontend_3, 'libssl3', '3_0_7_r0').
vulExists('CVE-2022-3996', 'libssl3', '3_0_7_r0', 'Network', 'A_loss', 'HIGH').
