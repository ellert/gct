/*
 * Copyright 1999-2017 University of Chicago
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "gssapi_test_utils.h"
#include <stdbool.h>
#include "openssl/ssl.h"

static gss_OID_desc tls_version_oid_desc =
     {11, "\x2b\x06\x01\x04\x01\x9b\x50\x01\x01\x01\x0b"};
static gss_OID_desc * tls_version_oid = &tls_version_oid_desc;

struct test_case
{
    const char *                        name;
    char *                              min_protocol;
    char *                              max_protocol;
    char *                              expected;
};

/**
 * @brief Test case for TLS version setting
 * @details
 *     In this test case, establish a security context and verify that the
 *     SSL version matches expected.
 */
bool
tls_test(const char *expected)
{
    OM_uint32                           major_status = GSS_S_COMPLETE;
    OM_uint32                           minor_status = GLOBUS_SUCCESS;
    gss_ctx_id_t                        init_context = GSS_C_NO_CONTEXT;
    gss_ctx_id_t                        accept_context = GSS_C_NO_CONTEXT;
    gss_buffer_desc                     init_generated_token = {0};
    gss_buffer_desc                     accept_generated_token = {0};
    bool                                result = true;
    OM_uint32                           ignore_minor_status = 0;
    const char                         *why = "";

    do
    {
        major_status = gss_init_sec_context(
                &minor_status,
                GSS_C_NO_CREDENTIAL,
                &init_context,
                GSS_C_NO_NAME,
                GSS_C_NO_OID,
                0,
                0,
                GSS_C_NO_CHANNEL_BINDINGS,
                &accept_generated_token,
                NULL,
                &init_generated_token,
                NULL,
                NULL);

        gss_release_buffer(
                &ignore_minor_status,
                &accept_generated_token);

        if (GSS_ERROR(major_status))
        {
            why = "gss_init_sec_context";
            result = false;
            break;
        }

        if (init_generated_token.length > 0)
        {
            major_status = gss_accept_sec_context(
                    &minor_status,
                    &accept_context,
                    GSS_C_NO_CREDENTIAL,
                    &init_generated_token,
                    GSS_C_NO_CHANNEL_BINDINGS,
                    NULL,
                    NULL,
                    &accept_generated_token,
                    NULL,
                    NULL,
                    NULL);
            gss_release_buffer(
                    &ignore_minor_status,
                    &init_generated_token);

            if (GSS_ERROR(major_status))
            {
                why = "accept_sec_context";
                result = false;
            }
        }
    }
    while (major_status == GSS_S_CONTINUE_NEEDED);

    if (major_status == GSS_S_COMPLETE)
    {
        gss_buffer_set_desc            *data = NULL;

        major_status = gss_inquire_sec_context_by_oid(
            &minor_status,
            accept_context,
            (gss_OID_desc *) tls_version_oid,
            &data);

        if (major_status != GSS_S_COMPLETE)
        {
            why = "inquire_context_by_oid";
            result = false;

            goto fail;
        }

        if (data->count != 1)
        {
            why = "inquire_result";
            result = false;
            goto fail;
        }
        if (strcmp(expected, data->elements[0].value) != 0)
        {
            why = globus_common_create_string(
                "expected %s, got %s",
                expected, data->elements[0].value);
            result = false;
            goto fail;
        }
    }

fail:
    if (major_status != GSS_S_COMPLETE)
    {
        globus_gsi_gssapi_test_print_error(
                stderr,
                major_status,
                minor_status);
    }

    if (init_context != GSS_C_NO_CONTEXT)
    {
        gss_delete_sec_context(
                &ignore_minor_status,
                &init_context,
                NULL);
    }
    if (accept_context != GSS_C_NO_CONTEXT)
    {
        gss_delete_sec_context(
                &ignore_minor_status,
                &accept_context,
                NULL);
    }
    if (init_generated_token.length != 0)
    {
        gss_release_buffer(
                &ignore_minor_status,
                &init_generated_token);
    }
    if (accept_generated_token.length != 0)
    {
        gss_release_buffer(
                &ignore_minor_status,
                &accept_generated_token);
    }

    if (!result)
    {
        fprintf(stderr, "Failed because %s\n", why);
    }

    return result;
}
/* tls_test() */

#define TEST_CASE_INITIALIZER(m, e) {e, m, m, e}

#if TLS_MAX_VERSION == TLS1_2_VERSION
#define TLSMAX "TLSv1.2"
#else
#define TLSMAX "TLSv1.3"
#endif

int
main(int argc, char *argv[])
{
    int                                 failed = 0;
    struct test_case                    test_cases[] =
    {
#if OPENSSL_VERSION_NUMBER < 0x30000010L
        TEST_CASE_INITIALIZER("TLS1_VERSION_DEPRECATED", "TLSv1"),
        TEST_CASE_INITIALIZER("TLS1_1_VERSION_DEPRECATED", "TLSv1.1"),
#endif
        TEST_CASE_INITIALIZER("TLS1_2_VERSION", "TLSv1.2"),
        TEST_CASE_INITIALIZER("TLS1_3_VERSION", TLSMAX),
        TEST_CASE_INITIALIZER("TLS1_VERSION", TLSMAX),
        TEST_CASE_INITIALIZER("TLS1_1_VERSION", TLSMAX),
        TEST_CASE_INITIALIZER("FOOBAR", TLSMAX),
    };
    size_t num_test_cases = sizeof(test_cases)/sizeof(test_cases[0]);
    printf("1..%zu\n", num_test_cases);

    for (size_t i = 0; i < num_test_cases; i++)
    {
        bool                            ok = false;
        globus_libc_setenv(
            "GLOBUS_GSSAPI_MIN_TLS_PROTOCOL", test_cases[i].min_protocol, 1);
        globus_libc_setenv(
            "GLOBUS_GSSAPI_MAX_TLS_PROTOCOL", test_cases[i].max_protocol, 1);

        globus_module_activate(GLOBUS_GSI_GSSAPI_MODULE);
        ok = tls_test(test_cases[i].expected);
        if (!ok)
        {
            printf("not ");
            failed++;
        }
        printf("ok %zu - %s\n",
                i+1,
                test_cases[i].name);
        globus_module_deactivate(GLOBUS_GSI_GSSAPI_MODULE);
    }
    exit(failed);
}
